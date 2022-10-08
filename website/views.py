"""Views for the website."""
import random
import string

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from website.forms import CustomCreationForm
from website.helpers import get_host_details, send_site_email
from website.models import Validation


def index(request) -> HttpResponse:
    """
    Handle the Index page.

    Args:
        request: HttpRequest object

    Return:
        HttpResponse for the index page
    """
    context = {"SUBDOMAIN": get_host_details(request=request).subdomain}
    return render(request, "website/index.html", context=context)


def register(request) -> HttpResponse:
    """
    Handle the registration process.

    Args:
        request: HttpRequest object

    Return:
        HttpResponse for the registration page
    """
    context: dict[str, str] = {}
    if request.method == "POST":
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            validation_string = "".join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                for _ in range(64)
            )
            user_validation = Validation(
                user=user, random_validation_string=validation_string
            )
            user_validation.save()

            host_details = get_host_details(request=request)

            subject: str = "Thank you for registering with devfaq"
            validate_url = f"{host_details.full_url}/validate?token={validation_string}"
            context = {
                "SITE_NAME": host_details.hostname,
                "VALIDATE_URL": validate_url,
            }
            message: str = render_to_string(
                template_name="email/registration.txt",
                context=context,
            )
            send_site_email(
                sender="no-reply@devfaq.com",
                recipient=user.email,
                subject=subject,
                message=message,
            )

            login(request, user)
            return redirect("/user_cp")
    else:
        form = CustomCreationForm()

    context = {
        "REGISTER_FORM": str(form.as_table),
    }
    return render(
        request=request, template_name="registration/register.html", context=context
    )


def email_validation(request) -> HttpResponse:
    """
    Handle the email validation process.

    Args:
        request: HttpRequest object

    Return:
        HttpResponse for the registration page
    """
    token = request.GET["token"]
    if not token:
        context = {
            "ERROR": "The URL is invalid. No token.",
        }
        return render(
            request=request, template_name="registration/error.html", context=context
        )

    try:
        user = User.objects.get(validation__random_validation_string=token)
    except User.DoesNotExist:
        context = {
            "ERROR": "Invalid token",
        }
        return render(
            request=request, template_name="registration/error.html", context=context
        )

    user.validation.random_validation_string = None
    user.validation.is_validated = True
    user.validation.save()

    return redirect("/user_cp")
