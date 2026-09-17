from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import BlogPost
from apps.portfolio.models import Category, Project
from apps.profiles.models import Service


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return ["core:home", "portfolio:work_home", "profiles:about", "profiles:experience",
                "profiles:services", "blog:post_list", "core:contact", "core:hire"]

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Category.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Project.objects.filter(is_published=True).select_related("category")

    def lastmod(self, obj):
        return obj.updated_at


class BlogPostSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return BlogPost.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    "static": StaticViewSitemap,
    "categories": CategorySitemap,
    "projects": ProjectSitemap,
    "blog": BlogPostSitemap,
}
