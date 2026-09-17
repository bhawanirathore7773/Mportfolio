from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Category, Project, Tag


def work_home(request):
    categories = Category.objects.filter(is_published=True).prefetch_related("projects__images")
    return render(request, "portfolio/work_home.html", {"categories": categories})


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    projects = (
        Project.objects.filter(category=category, is_published=True)
        .select_related("category")
        .prefetch_related("images", "tags")
    )

    query = request.GET.get("q", "").strip()
    if query:
        projects = projects.filter(title__icontains=query)

    tag_slug = request.GET.get("tag")
    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        projects = projects.filter(tags=active_tag)

    paginator = Paginator(projects, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    available_tags = Tag.objects.filter(projects__category=category).distinct()

    context = {
        "category": category,
        "page_obj": page_obj,
        "query": query,
        "available_tags": available_tags,
        "active_tag": active_tag,
    }
    return render(request, "portfolio/category_detail.html", context)


def project_detail(request, category_slug, project_slug):
    project = get_object_or_404(
        Project.objects.select_related("category").prefetch_related("images", "tags"),
        category__slug=category_slug, slug=project_slug, is_published=True,
    )
    related_projects = (
        Project.objects.filter(category=project.category, is_published=True)
        .exclude(pk=project.pk)
        .select_related("category")
        .prefetch_related("images")[:4]
    )
    context = {"project": project, "related_projects": related_projects}
    return render(request, "portfolio/project_detail.html", context)
