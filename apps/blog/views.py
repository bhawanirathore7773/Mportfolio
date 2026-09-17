from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import BlogCategory, BlogPost


def _published_posts():
    return (
        BlogPost.objects.filter(status="published", published_date__lte=timezone.now())
        .select_related("category")
    )


def post_list(request):
    posts = _published_posts()

    category_slug = request.GET.get("category")
    active_category = None
    if category_slug:
        active_category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=active_category)

    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    categories = BlogCategory.objects.filter(posts__in=_published_posts()).distinct()

    context = {"page_obj": page_obj, "categories": categories, "active_category": active_category}
    return render(request, "blog/blog_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(
        _published_posts().prefetch_related("related_projects"), slug=slug
    )
    related_posts = _published_posts().exclude(pk=post.pk)
    if post.category:
        related_posts = related_posts.filter(category=post.category)
    related_posts = related_posts[:3]

    context = {"post": post, "related_posts": related_posts}
    return render(request, "blog/blog_detail.html", context)
