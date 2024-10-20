"""Views for the website."""

import random
import string
from pathlib import Path
from typing import TypedDict

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from website.forms import CreateSite, CustomUserCreationForm
from website.helpers import (
    create_permissions,
    get_host_details,
    resize_image,
    send_site_email,
    user_add_permissions,
)
from website.models import Site, Validation


class IndexView(TemplateView):
    """Index View."""

    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        """
        Get the index page.

        Args:
            kwargs: Keyword arguments

        Returns: website/index.html with context
        """
        context = super().get_context_data(**kwargs)
        context["SUBDOMAIN"] = get_host_details(request=self.request).subdomain
        context["USER_SITES"] = []

        if self.request.user.is_authenticated:
            user_permissions = self.request.user.user_permissions.all()
            if user_permissions:
                user_sites: list[str] = []
                for user_permission in user_permissions:
                    user_permission_split = user_permission.codename.split("_")
                    user_sites.append(user_permission_split[0])
                context["USER_SITES"] = user_sites
        return context


class RegisterView(TemplateView):
    """Register View."""

    template_name = "registration/register.html"

    def get_context_data(self, **kwargs):
        """
        Get the registration page.

        Args:
            kwargs: Keyword arguments

        Returns: registration/register.html with context
        """
        context = super().get_context_data(**kwargs)
        context["FORM"] = CustomUserCreationForm()
        return context

    def post(self, request) -> HttpResponse:
        """
        Handle the registration process.

        Args:
            request: HttpRequest object

        Return:
            HttpResponse for the registration page
        """
        form = CustomUserCreationForm(request.POST)
        valid, response = process_form(
            form=form, request=request, redirect_url="/user_cp"
        )
        if valid:
            user = form.save()
            login(request, user)
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
        return response


class UserCpView(TemplateView):
    """User Control Panel View."""

    template_name = "website/user_cp.html"

    def get_context_data(self, **kwargs):
        """
        Get the user control panel.

        Args:
            kwargs: Keyword arguments

        Returns: website/user_cp.html with context
        """
        if not self.request.user.is_authenticated:
            return redirect("/accounts/login")

        context = super().get_context_data(**kwargs)
        sites = Site.objects.all()
        for site in sites:
            print(site.logo)
        return context


class ManageSiteView(TemplateView):
    """Manage Site."""

    template_name = "website/manage_site.html"

    def get_context_data(self, **kwargs):
        """
        Get the site details.

        Args:
            kwargs: Keyword arguments

        Returns: website/manage_site.html with context
        """
        if not self.request.user.is_authenticated:
            return redirect("/accounts/login")

        context = super().get_context_data(**kwargs)
        site = Site.objects.filter(subdomain=kwargs["site"])
        if len(site) == 0:
            return redirect("/create_site")
        # TODO Check user has permissions
        context["sites"] = site
        return context


def create_site(request) -> HttpResponse | JsonResponse:
    """
    Handle the creation site functionality.

    Args:
        request: HttpRequest object

    Return:
        HttpResponse for creating a site
    """
    if not request.user.is_authenticated:
        return redirect("/accounts/login")
    elif not request.user.validation.is_validated:
        return redirect("/user_cp")

    if request.method == "POST":
        create_site_form = CreateSite(request.POST, request.FILES, user=request.user)
        valid, response = process_form(
            form=create_site_form, request=request, redirect_url="/user_cp"
        )
        if valid:
            create_permissions(create_site_form.cleaned_data["subdomain"])
            user_add_permissions(
                user=request.user,
                subdomain=create_site_form.cleaned_data["subdomain"],
                permissions=["owner"],
            )
            site = Site.objects.get(
                subdomain=create_site_form.cleaned_data["subdomain"]
            )
            resized_logo = resize_image(
                image=Path(site.logo.name),
                new_name=f"{create_site_form.cleaned_data['subdomain']}.png",
                max_width=500,
                max_height=400,
            )
            site.logo.name = str(resized_logo)
            site.save()
        if response:
            return response
    else:
        create_site_form = CreateSite()
    context = {"FORM": create_site_form}
    return render(
        request=request, template_name="website/create_site.html", context=context
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
        user: User = User.objects.get(validation__random_validation_string=token)
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


def process_form(
    form, request, redirect_url: str
) -> tuple[bool, HttpResponse | JsonResponse | HttpResponseRedirect]:
    """
    Process a form to identify errors and identify output required.

    Args:
        form: Form to be processed
        request: Request that has the form data
        redirect_url: URL to redirect too on success

    Returns:
        Response to be provided to the user based on the result of validation
    """
    response: HttpResponse | JsonResponse | HttpResponseRedirect = HttpResponse(
        "Invalid request"
    )
    if form.is_valid():
        form.save()
        for accepted_type in request.accepted_types:
            if "application/json" == str(accepted_type):
                response = process_json_success(redirect_url=redirect_url)
                break
        if not response:
            response = redirect(redirect_url)
    else:
        for accepted_type in request.accepted_types:
            if "application/json" == str(accepted_type):
                response = process_json_failure(form.errors.as_data())
                break

    return bool(form.is_valid()), response


class JSONFailureResponse(TypedDict):
    """Typed dict to hold JSON failures."""

    result: str
    errors: dict[str, list[str]]


def process_json_failure(form_errors: dict[str, list[ValidationError]]) -> JsonResponse:
    """
    Process errors in a form.

    Args:
        form_errors: List of dictionary

    Returns:
        JsonResponse: Json response containing the result.
    """
    json_response: JSONFailureResponse = {
        "result": "failed",
        "errors": {},
    }

    for field, errors in form_errors.items():
        if field == "__all__":
            field = "non_field"
        error_list: list[str] = []
        for error in errors:
            error_list.append(str(error.message))
        json_response["errors"][field] = error_list
    return JsonResponse(json_response)


def process_json_success(redirect_url: str) -> JsonResponse:
    """
    Process successful form.

    Args:
        redirect_url: URL the user should be redirected too

    Returns:
        JsonResponse: Json response containing the result.
    """
    json_response = {
        "result": "success",
        "redirect": True,
        "redirect_url": redirect_url,
    }
    return JsonResponse(json_response)


def login_form(request) -> HttpResponse:
    """
    Handle the login process.

    Args:
        request: HttpRequest object
    Return:
        HttpResponse for the login page
    """
    # TODO update to adhere to the content type header as register does
    context: dict[str, CustomUserCreationForm | str] = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            json_success_response = {
                "result": "success",
                "redirect": True,
                "redirect_url": "/",
            }
            return JsonResponse(json_success_response)
        else:
            json_failure_response: JSONFailureResponse = {
                "result": "failed",
                "errors": {
                    "__all__": ["Login Failed"],
                },
            }
            return JsonResponse(json_failure_response)

    return render(
        request=request,
        template_name="registration/partials/login_form.html",
        context=context,
    )


def custom_login(request) -> HttpResponse:
    """
    Handle the login process.

    Args:
        request: HttpRequest object
    Return:
        HttpResponse for the registration page
    """
    # TODO update to adhere to the content type header as register does
    context: dict[str, CustomUserCreationForm | str] = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            json_success_response = {
                "result": "success",
                "redirect": True,
                "redirect_url": "/",
            }
            return JsonResponse(json_success_response)
        else:
            json_failure_response: JSONFailureResponse = {
                "result": "failed",
                "errors": {
                    "__all__": ["Login Failed"],
                },
            }
            return JsonResponse(json_failure_response)

    return render(
        request=request, template_name="registration/register.html", context=context
    )
