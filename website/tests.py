"""Tests for the website."""
from django.test import TestCase

from website import helpers


class Request:
    """Mocked version of a request object for testing."""

    META: dict[str, str]

    def __init__(self):
        """Initialise Request."""
        self.META = {}


class SubdomainTests(TestCase):
    """Tests to validate subdomain functionality."""

    def setUp(self) -> None:
        """Initialise test requirements."""
        self.dummy_request = Request()
        helpers.ALLOWED_HOSTS = ["devfaq.com"]

    def test_subdomain(self):
        """Test ensuring get_subdomain returns the correct subdomain."""
        host_details = [
            {"host": "python.devfaq.com", "expected_subdomain": "python"},
            {"host": "python.devfaq.com:8080", "expected_subdomain": "python"},
            {"host": "php.devfaq.com", "expected_subdomain": "php"},
            {"host": "devfaq.com", "expected_subdomain": ""},
            {"host": "devfaq.com:8080", "expected_subdomain": ""},
            {"host": "127.0.0.1", "expected_subdomain": ""},
            {"host": "127.0.0.1:8080", "expected_subdomain": ""},
            {"host": "other.domain.com", "expected_subdomain": ""},
            {"host": "other.domain.com:8080", "expected_subdomain": ""},
            {"host": "domain.com:8080", "expected_subdomain": ""},
            {"host": "domain.com", "expected_subdomain": ""},
            {"host": "domain", "expected_subdomain": ""},
        ]

        for host_detail in host_details:
            self.dummy_request.META["HTTP_HOST"] = host_detail["host"]
            self.assertEqual(
                helpers.get_subdomain(request=self.dummy_request),
                host_detail["expected_subdomain"],
            )
