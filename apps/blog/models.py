import math

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_image_file


class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(TimeStampedModel):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published"), ("scheduled", "Scheduled")]

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True, validators=[validate_image_file])
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts")
    author_name = models.CharField(max_length=100, default="Manish Kanwar")
    excerpt = models.CharField(max_length=240, blank=True)
    content = models.TextField(help_text="Main article body. Supports basic HTML for headings/links/images.")
    related_projects = models.ManyToManyField("portfolio.Project", blank=True, related_name="related_posts")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    published_date = models.DateTimeField(blank=True, null=True)

    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    canonical_url = models.URLField(blank=True)
    social_image = models.ImageField(upload_to="blog/social/", blank=True, null=True, validators=[validate_image_file])

    class Meta:
        ordering = ["-published_date", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == "published" and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def reading_time_minutes(self):
        word_count = len(self.content.split())
        return max(1, math.ceil(word_count / 200))

    @property
    def is_visible(self):
        return self.status == "published" and self.published_date and self.published_date <= timezone.now()
