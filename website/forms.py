"""Forms for registration."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import EmailField


class CustomCreationForm(UserCreationForm):
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
        for fieldname in ("username", "email", "password1", "password2"):
            self.fields[fieldname].help_text = None

    class META:
        """Override the fields that are required."""

        model = User
        field = ("username", "email", "password1", "password2")

    def clean(self):
        """
        Validate form fields.

        Returns:
            Cleaned form fields
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use")
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Please choose a different username")
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
