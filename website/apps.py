"""App config for the website."""
from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """Class to handle the Django config for the website."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "website"
