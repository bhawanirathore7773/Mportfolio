from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render

from apps.blog.models import BlogPost
from apps.portfolio.models import Category, Project
from apps.profiles.models import Service

from .emails import send_contact_notifications, send_hire_notifications
from .forms import ContactForm, HireRequestForm
from .models import HomepageSettings, ProcessStep, Testimonial


def home(request):
    homepage = HomepageSettings.load()
    categories = Category.objects.filter(is_published=True).prefetch_related("projects")[:5]
    featured_projects = (
        Project.objects.filter(is_published=True, is_featured=True)
        .select_related("category")
        .prefetch_related("images")[:6]
    )
    services = Service.objects.filter(is_published=True)[:6]
    process_steps = ProcessStep.objects.all()
    recent_posts = BlogPost.objects.filter(status="published").select_related("category")[:3]
    testimonials = Testimonial.objects.filter(is_published=True)

    context = {
        "homepage": homepage,
        "categories": categories,
        "featured_projects": featured_projects,
        "services": services,
        "process_steps": process_steps,
        "recent_posts": recent_posts,
        "testimonials": testimonials,
    }
    return render(request, "home.html", context)


def health_check(request):
    """Lightweight deployment health endpoint that does not require the database."""
    return JsonResponse({"status": "ok"})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        inquiry = form.save()
        send_contact_notifications(inquiry)
        messages.success(request, "Thank you for reaching out. Your message has been received.")
        return redirect("core:contact")
    return render(request, "contact.html", {"form": form})


def hire(request):
    form = HireRequestForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        hire_request = form.save()
        send_hire_notifications(hire_request)
        messages.success(
            request, "Thank you for reaching out. Your project enquiry has been received successfully."
        )
        return redirect("core:hire")
    return render(request, "hire.html", {"form": form})


def privacy_policy(request):
    return render(request, "legal/privacy.html")


def terms(request):
    return render(request, "legal/terms.html")


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /private/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def handler404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def handler403(request, exception=None):
    return render(request, "errors/403.html", status=403)


def handler500(request):
    return render(request, "errors/500.html", status=500)
