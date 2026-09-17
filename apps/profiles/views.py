from django.shortcuts import render

from .models import Experience, Service, Skill


def about(request):
    skills = Skill.objects.all()
    return render(request, "about.html", {"skills": skills})


def experience(request):
    experiences = Experience.objects.all()
    return render(request, "experience.html", {"experiences": experiences})


def services(request):
    service_list = Service.objects.filter(is_published=True)
    return render(request, "services.html", {"services": service_list})
