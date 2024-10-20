"""Code to add the functionality to add dummy data for testing."""

from django import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from model_bakery import baker

from website.models import Site


class Command(BaseCommand):
    """Command to populate the database with dummy data."""

    help = "Load the database with dummy data."

    def add_arguments(self, parser) -> None:
        """
        Add argument to clear database.

        Args:
            parser: Instance of ArgumentParser.
        """
        parser.add_argument(
            "clear",
            type=bool,
            nargs="?",
            default=False,
            help="Clear existing data in the database.",
        )

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        """
        Perform the dummy data loading.

        Args:
            args: Positional arguments.
            options: Keyword arguments derived from argparse.
        """
        if options["clear"]:
            self._clear_database()

        self._populate_database()

    def _clear_database(self) -> None:
        """Clear the database."""
        self.stdout.write()
        self.stdout.write("Clearing database...")
        for app in apps.apps.get_models(
            include_auto_created=True, include_swapped=True
        ):
            app.objects.all().delete()
            self.stdout.write(f"...Deleted content for {app.__name__}")

    def _populate_database(self) -> None:
        """Populate the database with dummy data."""
        self.stdout.write()
        self.stdout.write("Loading dummy data...")
        baker.make(Site)
        self.stdout.write()
