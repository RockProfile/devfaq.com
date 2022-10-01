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
    hostname_split = hostname.split(".")
    subdomain = hostname_split[0]
    full_host = hostname.split(":")[0]
    if len(hostname_split) < 3 or full_host in ALLOWED_HOSTS or subdomain.isdigit():
        return ""
    return subdomain
