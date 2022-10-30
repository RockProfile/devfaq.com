"""URL configuration for the network application."""
from django.urls import include, path

from website import views

app_name = "network"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("create_site", views.create_site, name="create_site"),
    path("register", views.register, name="register"),
    path("register_form", views.register_form, name="register_form"),
    path("login", views.custom_login, name="login"),
    path("login_form", views.login_form, name="login_form"),
    path("user_cp", views.user_cp, name="user_control_panel"),
    path("validate", views.email_validation, name="email_validation"),
]
