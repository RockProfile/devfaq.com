"""Models for the website."""

from django.contrib.auth.models import User
from django.db import models

from website.validators import file_size_validator, subdomain_validator

PLUGINS = (
    ("article", "Article"),
    ("calendar", "Calendar"),
    ("faq", "FAQ"),
    ("featured_function", "Featured Function"),
    ("featured_package", "Featured Package"),
    ("news", "News"),
)


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
    new_filename: str = f"{path}{instance.subdomain}.{ext}"
    return new_filename


class BiographyModel(models.Model):
    """Model to store user Biography information."""

    for_user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    website: models.URLField = models.URLField(max_length=255, blank=True, null=True)
    biography: models.CharField = models.CharField(
        max_length=1000, blank=False, null=False
    )


class Socials(models.Model):
    """Model to store social medai links."""

    name: models.CharField = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=(
            ("facebook", "Facebook"),
            ("linkedin", "LinkedIn"),
            ("mastodon", "Mastodon"),
            ("x", "X"),
        ),
    )
    for_user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    handle: models.CharField = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        """Metaclass to add constraints."""

        constraints = [
            models.UniqueConstraint(
                fields=["name", "for_user"],
                name="unique_socials",
            )
        ]


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
    name = models.CharField(
        max_length=50,
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


class PluginContent(models.Model):
    """Model to handle plugin content."""

    author: models.ForeignKey(User, on_delete=models.CASCADE)
    published_on: models.DateField = models.DateField(auto_now_add=True)
    plugin: models.CharField = models.CharField(choices=PLUGINS, max_length=100)
    content: models.JSONField = models.JSONField(default=dict)
    draft: models.BooleanField = models.BooleanField(default=False)
    for_site: models.ForeignKey = models.ForeignKey(Site, on_delete=models.CASCADE)
