from django.contrib import admin

from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "published_date", "reading_time_minutes")
    list_filter = ("status", "category")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("related_projects",)
    fieldsets = (
        ("General", {"fields": ("title", "slug", "featured_image", "category", "author_name", "excerpt", "content")}),
        ("Related", {"fields": ("related_projects",)}),
        ("SEO", {"fields": ("seo_title", "seo_description", "canonical_url", "social_image")}),
        ("Publishing", {"fields": ("status", "published_date")}),
    )
