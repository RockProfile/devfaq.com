"""Models for the website."""
from django.conf import settings
from django.contrib.auth.models import User
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


class Validation(models.Model):
    """Model to handle user validation."""

    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    is_validated: models.BooleanField = models.BooleanField(default=False)
    random_validation_string: models.CharField = models.CharField(
        max_length=64, blank=True, null=True
    )


class PermissionManagement(models.Model):
    """Class created purely for permission management."""

    class META:
        """Meta class setting up PermissionManagement."""

        managed = False
        default_permissions = ()
