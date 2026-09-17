from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_image_file


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="categories/", blank=True, null=True, validators=[validate_image_file])

    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)

    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:category_detail", kwargs={"category_slug": self.slug})

    @property
    def published_project_count(self):
        return self.projects.filter(is_published=True).count()


class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(TimeStampedModel):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="projects")
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")

    short_description = models.CharField(max_length=220, blank=True)
    description = models.TextField(
        blank=True, help_text="Longer, SEO-friendly project overview shown on the project page."
    )

    # Design Information — only fields with real data are shown on the page.
    design_type = models.CharField(max_length=120, blank=True)
    technique = models.CharField(max_length=120, blank=True)
    application = models.CharField(max_length=120, blank=True)
    style = models.CharField(max_length=120, blank=True)
    software = models.CharField(max_length=120, blank=True)
    color_direction = models.CharField(max_length=120, blank=True)
    year = models.PositiveIntegerField(blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        unique_together = [("category", "slug")]
        indexes = [models.Index(fields=["is_published", "is_featured"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "portfolio:project_detail",
            kwargs={"category_slug": self.category.slug, "project_slug": self.slug},
        )

    @property
    def cover_image(self):
        first = self.images.order_by("display_order").first()
        return first.image if first else None

    @property
    def design_info(self):
        """Only the design-information fields that actually have a value —
        the template loops over this instead of hard-coding every row.
        """
        fields = [
            ("Category", self.category.name),
            ("Design Type", self.design_type),
            ("Technique", self.technique),
            ("Application", self.application),
            ("Style", self.style),
            ("Software", self.software),
            ("Color Direction", self.color_direction),
            ("Year", self.year),
        ]
        return [(label, value) for label, value in fields if value]


class ProjectImage(TimeStampedModel):
    IMAGE_TYPE_CHOICES = [
        ("main", "Main Design"),
        ("motif", "Motif"),
        ("top", "Top / Placement"),
        ("bottom", "Bottom / Border"),
        ("border", "Border"),
        ("repeat", "Repeat / Surface"),
        ("detail", "Detail"),
        ("back", "Back"),
        ("side", "Side"),
        ("colorway", "Colorway"),
        ("mockup", "Mockup"),
        ("other", "Other"),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/", validators=[validate_image_file])
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, default="detail")
    title = models.CharField(max_length=120, blank=True)
    description = models.TextField(max_length=400, blank=True)
    alt_text = models.CharField(
        max_length=160, blank=True,
        help_text="Descriptive alt text for SEO/accessibility, e.g. 'Floral botanical surface pattern textile design'.",
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.project.title} — {self.get_image_type_display()}"

    @property
    def effective_alt_text(self):
        return self.alt_text or self.title or f"{self.project.title} — {self.project.category.name}"
