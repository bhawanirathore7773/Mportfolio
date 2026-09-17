from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.work_home, name="work_home"),
    path("<slug:category_slug>/", views.category_detail, name="category_detail"),
    path("<slug:category_slug>/<slug:project_slug>/", views.project_detail, name="project_detail"),
]
