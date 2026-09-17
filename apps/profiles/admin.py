from django.contrib import admin

from .models import Experience, Service, Skill


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "is_current", "display_order")
    list_editable = ("display_order",)
    list_filter = ("is_current",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "display_order")
    list_editable = ("display_order",)
    list_filter = ("category",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "display_order")
    list_editable = ("is_published", "display_order")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("General", {"fields": ("title", "slug", "icon", "short_description", "detailed_description")}),
        ("Details", {"fields": ("deliverables", "ideal_for")}),
        ("Publishing", {"fields": ("is_published", "display_order")}),
    )
