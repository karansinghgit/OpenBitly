from django.urls import path

from . import views

urlpatterns = [
    path("api/shorten", views.shorten),
]
