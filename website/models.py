"""Models for the website."""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from website.validators import file_size_validator, subdomain_validator


def logo_file_name(instance: "Site", filename: str) -> str:
    """
    Calculate the expected filename for a site logo.

    Args:
        instance: Site object being added/updated
        filename: Original filename for the logo

    Returns: Path and name of the logo file
    """
    path: str = "static/logos/"
    ext: str = filename.split(".")[-1]
    return f"{path}{instance.subdomain}.{ext}"


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


class PermissionManagement(models.Model):
    """Class created purely for permission management."""

    class META:
        """Meta class setting up PermissionManagement."""

        managed = False
        default_permissions = ()


class Site(models.Model):
    """Model for the subdomains."""

    subdomain: models.CharField = models.CharField(
        unique=True,
        max_length=20,
        validators=[subdomain_validator],
        blank=False,
        null=False,
    )
    description: models.TextField = models.TextField(
        max_length=2000,
        blank=False,
        null=False,
    )
    logo: models.ImageField = models.ImageField(
        upload_to=logo_file_name,
        null=True,
        blank=True,
        validators=[file_size_validator],
    )
    live: models.BooleanField = models.BooleanField(
        default=False,
        blank=False,
        null=False,
    )
    created_by: models.ForeignKey = models.ForeignKey(
        to=User,
        blank=True,
        null=True,
        on_delete=models.RESTRICT,
    )


class Validation(models.Model):
    """Model to handle user validation."""

    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    is_validated: models.BooleanField = models.BooleanField(default=False)
    random_validation_string: models.CharField = models.CharField(
        max_length=64, blank=True, null=True
    )
