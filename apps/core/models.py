from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_cv_file, validate_image_file

phone_validator = RegexValidator(
    regex=r"^[0-9+\-\s()]{7,20}$", message="Enter a valid phone number."
)


class TimeStampedModel(models.Model):
    """Abstract base adding created_at / updated_at to any model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    """Abstract base for models that should only ever have one row
    (site-wide settings, homepage content). Always saves to pk=1 and
    exposes .load() so templates/views can fetch-or-create it safely.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singleton rows are never deleted, only edited

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    """Global, site-wide settings editable from one place in the admin."""

    site_name = models.CharField(max_length=120, default="Manish Kanwar")
    tagline = models.CharField(max_length=200, blank=True, default="Textile Designer & CAD Designer")
    logo = models.ImageField(upload_to="site/", blank=True, null=True, validators=[validate_image_file])
    favicon = models.ImageField(upload_to="site/", blank=True, null=True, validators=[validate_image_file])

    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    location = models.CharField(max_length=120, blank=True, help_text="e.g. Jaipur, Rajasthan, India")

    cv_file = models.FileField(
        upload_to="documents/", blank=True, null=True, validators=[validate_cv_file],
        help_text="PDF shown behind the 'Download CV' button.",
    )

    open_to_freelance = models.BooleanField(
        default=False, help_text="Shows the 'currently open to freelance projects' note in the hero."
    )
    available_for_opportunities = models.BooleanField(
        default=False, help_text="Shows the 'Available for Professional Opportunities' section site-wide."
    )

    # Global SEO defaults — individual pages/projects/posts can override these.
    default_seo_title = models.CharField(max_length=70, blank=True)
    default_seo_description = models.CharField(max_length=160, blank=True)
    default_og_image = models.ImageField(upload_to="site/", blank=True, null=True, validators=[validate_image_file])

    google_analytics_id = models.CharField(max_length=32, blank=True, help_text="e.g. G-XXXXXXXXXX")
    google_search_console_code = models.CharField(max_length=200, blank=True)

    footer_note = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"


class SocialLink(TimeStampedModel):
    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("behance", "Behance"),
        ("pinterest", "Pinterest"),
        ("facebook", "Facebook"),
        ("email", "Email"),
        ("other", "Other"),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    label = models.CharField(max_length=60, blank=True, help_text="Optional custom label, e.g. 'Behance'")
    url = models.URLField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.label or self.get_platform_display()


class HomepageSettings(SingletonModel):
    """Editable copy blocks for the homepage sections (hero, intro, final CTA)."""

    hero_title = models.CharField(max_length=200, default="Textile Designer & CAD Designer")
    hero_subtitle = models.TextField(
        max_length=300,
        default="Creating contemporary textile designs, surface patterns and CAD artwork for fashion and textile applications.",
    )
    hero_badge_text = models.CharField(max_length=80, blank=True, default="2+ Years of Professional Experience")
    hero_primary_cta_text = models.CharField(max_length=40, default="View My Work")
    hero_primary_cta_link = models.CharField(max_length=200, default="/work/")
    hero_secondary_cta_text = models.CharField(max_length=40, default="Hire Me")
    hero_secondary_cta_link = models.CharField(max_length=200, default="/hire/")
    hero_image = models.ImageField(upload_to="homepage/", blank=True, null=True, validators=[validate_image_file])
    hero_secondary_image = models.ImageField(upload_to="homepage/", blank=True, null=True, validators=[validate_image_file])

    intro_heading = models.CharField(max_length=200, default="Designing Ideas Into Textile Stories.")
    intro_content = models.TextField(
        default=(
            "I am a Textile Designer and CAD Designer with 2+ years of professional experience "
            "creating textile prints, surface patterns and digital design concepts. My work "
            "combines creative exploration with an understanding of contemporary trends, visual "
            "balance and practical textile applications."
        )
    )

    work_section_heading = models.CharField(max_length=120, default="Selected Work")
    work_section_subtitle = models.CharField(
        max_length=240,
        default="A curated selection of textile designs developed across different styles, techniques and applications.",
    )

    final_cta_heading = models.CharField(max_length=200, default="Have a Textile Design Project in Mind?")
    final_cta_description = models.TextField(
        default=(
            "Whether you need a custom textile print, surface pattern, CAD artwork or a complete "
            "design direction, let's discuss your requirements."
        )
    )

    class Meta:
        verbose_name = "Homepage Settings"
        verbose_name_plural = "Homepage Settings"

    def __str__(self):
        return "Homepage Settings"


class ProcessStep(TimeStampedModel):
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=300)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "step_number"]

    def __str__(self):
        return f"{self.step_number:02d} — {self.title}"


class Testimonial(TimeStampedModel):
    """Only ever populated with real, verifiable feedback — never seeded
    with placeholder quotes. The homepage/about templates hide this
    section entirely when no published testimonials exist.
    """

    author_name = models.CharField(max_length=120)
    author_role = models.CharField(max_length=160, blank=True, help_text="Role / company")
    quote = models.TextField(max_length=500)
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True, validators=[validate_image_file])
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.author_name} — {self.author_role}"


class ContactInquiry(TimeStampedModel):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("in_discussion", "In Discussion"),
        ("converted", "Converted"),
        ("closed", "Closed"),
    ]
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} ({self.created_at:%d %b %Y})"


class HireRequest(TimeStampedModel):
    STATUS_CHOICES = ContactInquiry.STATUS_CHOICES
    PROJECT_TYPE_CHOICES = [
        ("textile_print", "Textile Print Design"),
        ("cad", "CAD Design"),
        ("surface_pattern", "Surface Pattern Design"),
        ("digital_textile", "Digital Textile Design"),
        ("motif", "Motif Development"),
        ("repeat", "Repeat Pattern"),
        ("collection", "Collection Development"),
        ("custom", "Custom Design"),
        ("other", "Other"),
    ]
    CONTACT_METHOD_CHOICES = [("email", "Email"), ("phone", "Phone"), ("whatsapp", "WhatsApp")]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=160, blank=True)
    project_type = models.CharField(max_length=30, choices=PROJECT_TYPE_CHOICES)
    budget_range = models.CharField(max_length=80, blank=True)
    timeline = models.CharField(max_length=80, blank=True)
    project_details = models.TextField()
    reference_file = models.FileField(upload_to="hire_references/", blank=True, null=True)
    preferred_contact_method = models.CharField(max_length=20, choices=CONTACT_METHOD_CHOICES, default="email")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.get_project_type_display()}"
