"""URL configuration for the network application."""

from django.urls import include, path

from website import views

app_name = "network"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("create_site", views.create_site, name="create_site"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.custom_login, name="login"),
    path("login_form", views.login_form, name="login_form"),
    path("user_cp", views.UserCpView.as_view(), name="user_control_panel"),
    path("validate", views.email_validation, name="email_validation"),
]
