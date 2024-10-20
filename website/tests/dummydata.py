"""Module to create dummy data."""

from model_bakery import baker

from website.models import User

baker.make(User)
