"""URL configuration for the network application."""
from django.urls import path

from website import views

app_name = "network"
urlpatterns = [
    path("", views.index, name="index"),
]
