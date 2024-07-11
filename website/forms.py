"""Forms for registration."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import EmailField

from website.models import Site


class CreateSite(forms.ModelForm):
    """Form to handle creating sites."""

    def __init__(self, *args, **kwargs):
        """
        Initialize CreateSite.

        Args:
            args: Positional arguments
            kwargs: Keyword arguments
        """
        self.user = ""
        if "user" in kwargs:
            self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        for field_name in ("subdomain", "description", "logo"):
            self.fields[field_name].help_text = None

    class Meta:
        """Override the fields that are required."""

        model = Site
        fields = ("subdomain", "description", "logo")

    def clean(self):
        """Validate the form."""
        try:
            Site.objects.get(subdomain=self.cleaned_data.get("subdomain"))
            self.add_error("subdomain", ValidationError("The subdomain already exists"))
        except Site.DoesNotExist:
            pass
        return self.cleaned_data

    def save(self, commit=True):
        """
        Override the save function to include the created_by field.

        Args:
            commit: True to commit changes after save
        """
        site = super().save(commit=False)
        site.created_by = self.user
        if commit:
            site.save()
        return site


class CustomUserCreationForm(UserCreationForm):
    """Custom registration form."""

    email = EmailField(required=True)

    def __init__(self, *args, **kwargs):
        """
        Initialize CustomCreationForm.

        Args:
            args: Positional arguments
            kwargs: Keyword arguments
        """
        super().__init__(*args, **kwargs)
        for field_name in ("username", "email", "password1", "password2"):
            self.fields[field_name].help_text = None

    def clean(self):
        """
        Validate form fields.

        Returns:
            Cleaned form fields
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error("email", ValidationError("Email is already in use"))
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            self.add_error(
                "username", ValidationError("Please choose a different username")
            )
        return self.cleaned_data

    def save(self, commit=True):
        """
        Override the save function to include the email field.

        Args:
            commit: True to commit changes after save
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
