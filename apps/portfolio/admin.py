from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Project, ProjectImage, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "display_order", "is_published", "published_project_count")
    list_editable = ("display_order", "is_published")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("preview", "image", "image_type", "title", "alt_text", "display_order")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return "—"

    preview.short_description = "Preview"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "is_featured", "display_order", "year")
    list_editable = ("is_published", "is_featured", "display_order")
    list_filter = ("category", "is_published", "is_featured", "tags")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category",)
    filter_horizontal = ("tags",)
    inlines = [ProjectImageInline]

    fieldsets = (
        ("General", {"fields": ("title", "slug", "category", "tags", "short_description", "description")}),
        ("Design Information", {
            "fields": ("design_type", "technique", "application", "style", "software", "color_direction", "year")
        }),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
        ("Publishing", {"fields": ("is_published", "is_featured", "display_order")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category").prefetch_related("tags", "images")


admin.site.site_header = "Manish Kanwar — Studio Dashboard"
admin.site.site_title = "Studio Dashboard"
admin.site.index_title = "Welcome back, Manish"
