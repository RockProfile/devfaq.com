"""Models for the website."""
from django.conf import settings
from django.db import models


class BiographyModel(models.Model):
    """Model to store user Biography information."""

    for_user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    twitter: models.CharField = models.CharField(max_length=15, blank=True, null=True)
    website: models.URLField = models.URLField(max_length=255, blank=True, null=True)
    biography: models.CharField = models.CharField(
        max_length=1000, blank=False, null=False
    )
