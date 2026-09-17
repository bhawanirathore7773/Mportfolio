from django.contrib import admin

from .models import (
    ContactInquiry,
    HireRequest,
    HomepageSettings,
    ProcessStep,
    SiteSettings,
    SocialLink,
    Testimonial,
)


class SingletonAdmin(admin.ModelAdmin):
    """Hides the add/delete actions for singleton settings models and
    always redirects straight to the single existing row."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Identity", {"fields": ("site_name", "tagline", "logo", "favicon")}),
        ("Contact", {"fields": ("contact_email", "contact_phone", "location")}),
        ("CV & Availability", {"fields": ("cv_file", "open_to_freelance", "available_for_opportunities")}),
        ("Default SEO", {"fields": ("default_seo_title", "default_seo_description", "default_og_image")}),
        ("Analytics", {"fields": ("google_analytics_id", "google_search_console_code")}),
        ("Footer", {"fields": ("footer_note",)}),
    )


@admin.register(HomepageSettings)
class HomepageSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Hero", {
            "fields": (
                "hero_title", "hero_subtitle", "hero_badge_text",
                "hero_primary_cta_text", "hero_primary_cta_link",
                "hero_secondary_cta_text", "hero_secondary_cta_link",
                "hero_image", "hero_secondary_image",
            )
        }),
        ("Introduction", {"fields": ("intro_heading", "intro_content")}),
        ("Selected Work section", {"fields": ("work_section_heading", "work_section_subtitle")}),
        ("Final call to action", {"fields": ("final_cta_heading", "final_cta_description")}),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "label", "url", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("platform", "is_active")


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("step_number", "title", "display_order")
    list_editable = ("display_order",)
    ordering = ("display_order",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_role", "is_published", "display_order")
    list_editable = ("display_order", "is_published")
    list_filter = ("is_published",)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "phone", "message", "created_at")


@admin.register(HireRequest)
class HireRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "project_type", "budget_range", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "project_type", "created_at")
    search_fields = ("full_name", "email", "company", "project_details")
    readonly_fields = (
        "full_name", "email", "phone", "company", "project_type", "budget_range",
        "timeline", "project_details", "reference_file", "preferred_contact_method", "created_at",
    )
