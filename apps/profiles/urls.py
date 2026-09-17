from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("about/", views.about, name="about"),
    path("experience/", views.experience, name="experience"),
    path("services/", views.services, name="services"),
]
