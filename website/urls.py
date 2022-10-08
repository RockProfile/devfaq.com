"""URL configuration for the network application."""
from django.urls import include, path

from website import views

app_name = "network"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register", views.register, name="register"),
    path("validate", views.email_validation, name="email_validation"),
]
