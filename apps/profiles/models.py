from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_image_file


class Experience(TimeStampedModel):
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    responsibilities = models.TextField(
        blank=True, help_text="One responsibility per line — shown as a bullet list."
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-start_date"]
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.role} — {self.company}"

    @property
    def responsibility_list(self):
        return [line.strip() for line in self.responsibilities.splitlines() if line.strip()]


class Skill(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("design", "Design"),
        ("software", "Software / Tools"),
        ("technique", "Technique"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="design")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Service(TimeStampedModel):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True, unique=True)
    icon = models.CharField(
        max_length=40, blank=True,
        help_text="Optional short icon keyword used by the template (e.g. 'pattern', 'cad', 'digital').",
    )
    short_description = models.CharField(max_length=220)
    detailed_description = models.TextField(blank=True)
    deliverables = models.TextField(blank=True, help_text="One deliverable per line.")
    ideal_for = models.TextField(blank=True, help_text="One audience/use-case per line.")
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"{reverse('profiles:services')}#{self.slug}"

    @property
    def deliverable_list(self):
        return [line.strip() for line in self.deliverables.splitlines() if line.strip()]

    @property
    def ideal_for_list(self):
        return [line.strip() for line in self.ideal_for.splitlines() if line.strip()]
