"""Validators to use for forms and models."""
from re import match

from django.core.exceptions import ValidationError


def file_size_validator(file_field):
    """
    Validate the size of the file.

    Args:
        file_field: File field to validate

    Raises:
        ValidationError: On validation issue
    """
    file_size = file_field.file.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Upload exceeds the maximum file size of {limit_mb}MB")


def subdomain_validator(subdomain: str):
    """
    Validate subdomains.

    Args:
        subdomain: Subdomain to validate

    Raises:
        ValidationError: On validation issue
    """
    regex = r"^[a-zA-Z][a-zA-Z0-9-]+[a-zA-Z0-9]$"
    if not match(regex, subdomain):
        raise ValidationError(
            "The requested subdomain is invalid, "
            "it must start and end with a letter and only contain letters numbers and hyphens"
        )
