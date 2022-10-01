"""Helper functions."""
from devfaq.settings import ALLOWED_HOSTS


def get_subdomain(request) -> str:
    """
    Parse the subdomain from the request.

    Args:
        request: Request object received from a view

    Returns:
        The subdomain as a string, if a subdomain cannot be found then an empty string is returns
    """
    try:
        hostname = request.META["HTTP_HOST"]
    except KeyError:
        return ""

    full_host = hostname.split(":")[0]
    if full_host in ALLOWED_HOSTS:
        return ""

    full_host_split = full_host.split(".")
    subdomain = full_host_split[0]

    if len(full_host_split) < 3 or subdomain.isdigit():
        return ""

    domain_part = ".".join(full_host_split[1:])

    if domain_part not in ALLOWED_HOSTS:
        return ""
    return subdomain
