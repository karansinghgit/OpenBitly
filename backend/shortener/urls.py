from django.urls import path

from . import views

urlpatterns = [
    path("api/shorten", views.shorten),
    path("<str:code>", views.resolve),  # catch-all: keep last
]
