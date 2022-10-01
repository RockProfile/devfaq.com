"""Views for the website."""
from django.http import HttpResponse
from django.shortcuts import render

from website.helpers import get_subdomain


def index(request) -> HttpResponse:
    """
    Handle the Index page.

    Args:
        request: HttpRequest object

    Return:
        HttpResponse for the rack page
    """
    context = {"SUBDOMAIN": get_subdomain(request=request)}
    return render(request, "website/index.html", context=context)
