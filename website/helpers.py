"""Helper functions and classes."""
from dataclasses import dataclass

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail

from devfaq.settings import ALLOWED_HOSTS
from website.models import PermissionManagement


@dataclass
class HostDetails:
    """Class to hold host details."""

    scheme: str = ""
    subdomain: str = ""
    hostname: str = ""
    port: int = 443
    full_url: str = ""


def create_permissions(subdomain: str):
    """
    Create permission set for subdomain.

    Args:
        subdomain: Subdomain to create permission set for
    """
    content_type = ContentType.objects.get_for_model(PermissionManagement)
    Permission.objects.create(
        codename=f"{subdomain}_owner",
        name=f"Owner of {subdomain}",
        content_type=content_type,
    )
    Permission.objects.create(
        codename=f"{subdomain}_contributor",
        name=f"Contributor to {subdomain}",
        content_type=content_type,
    )


def delete_permissions(subdomain: str):
    """
    Delete permissions for a subdomain.

    Args:
        subdomain: Subdomain to delete permissions for.
    """
    content_type = ContentType.objects.get_for_model(PermissionManagement)
    Permission.objects.filter(
        content_type=content_type,
        codename__in=(f"{subdomain}_contributor", f"{subdomain}_owner"),
    ).delete()


def user_add_permissions(user: User, subdomain: str, permissions: list[str]):
    """
    Add permissions to the given user.

    Args:
        user: The user to add permissions for
        subdomain: The subdomain the permission is for
        permissions: List of permissions to add (can be owner or contributor)
    """
    content_type = ContentType.objects.get_for_model(PermissionManagement)
    for permission in permissions:
        try:
            permission_db = Permission.objects.get(
                content_type=content_type, codename=f"{subdomain}_{permission}"
            )
            user.user_permissions.add(permission_db)
            user.save()
        except Permission.DoesNotExist:
            pass


def user_remove_permissions(user: User, subdomain: str, permissions: list[str]):
    """
    Remove permissions from the given user.

    Args:
        user: The user to remove permissions for
        subdomain: The subdomain the permission is for
        permissions: List of permissions to remove (can be owner or contributor)
    """
    content_type = ContentType.objects.get_for_model(PermissionManagement)
    for permission in permissions:
        try:
            permission_db = Permission.objects.get(
                content_type=content_type, codename=f"{subdomain}_{permission}"
            )
            user.user_permissions.remove(permission_db)
            user.save()
        except Permission.DoesNotExist:
            pass


def get_host_details(request) -> HostDetails:
    """
    Parse the host details.

    Args:
        request: Request object received from a view

    Returns:
        Dictionary containing the main host parts
    """
    host_details = HostDetails()
    host_details.scheme = request.scheme
    try:
        hostname = request.META["HTTP_HOST"]
    except KeyError:
        return host_details

    allowed_hosts = []
    for allow_host in ALLOWED_HOSTS:
        if allow_host.startswith("."):
            allowed_hosts.append(allow_host[1:])
            continue
        allowed_hosts.append(allow_host)

    host_details.hostname = hostname
    hostname_split = hostname.split(":")
    hostname_no_port = hostname_split[0]

    if len(hostname_split) > 1:
        host_details.port = int(hostname_split[1])
    elif host_details.scheme == "http":
        host_details.port = 80

    subdomain = hostname_no_port.split(".")[0]
    hostname_without_subdomain = hostname_no_port[len(subdomain) + 1 :]
    if (
        hostname_no_port in allowed_hosts
        or hostname_without_subdomain not in allowed_hosts
    ):
        host_details.hostname = hostname_no_port
    else:
        host_details.hostname = hostname_without_subdomain
        host_details.subdomain = subdomain
    subdomain = f"{host_details.subdomain}." if host_details.subdomain else ""
    port = ""
    if (host_details.scheme != "https" or host_details.port != 443) and (
        host_details.scheme != "http" or host_details.port != 80
    ):
        port = f":{host_details.port}"
    full_url = f"{host_details.scheme}://{subdomain}{host_details.hostname}{port}"
    host_details.full_url = full_url
    return host_details


def send_site_email(sender: str, recipient: str, subject: str, message: str):
    """
    Send email.

    Args:
        sender: Email address to send from
        recipient: Email address to send too
        subject: Subject for the email
        messgae: Body of the email
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=sender,
        recipient_list=[recipient],
        fail_silently=False,
    )
