"""Tests for the website."""

from django.test import TestCase

from devfaq.settings import BASE_DIR
from website import helpers

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


class Request:
    """Mocked version of a request object for testing."""

    META: dict[str, str]

    _scheme = ""

    def __init__(self):
        """Initialise Request."""
        self.META = {}

    @property
    def scheme(self) -> str:
        """Mock the scheme."""
        return self._scheme

    @scheme.setter
    def scheme(self, scheme: str):
        """Mock the scheme."""
        self._scheme = scheme

    def get_host(self) -> str:
        """Mock the get_host method."""
        # TODO fix so that this is actually using the behaviour of the real method
        return self.META["HTTP_HOST"]


class SubdomainTests(TestCase):
    """Tests to validate subdomain functionality."""

    def setUp(self) -> None:
        """Initialise test requirements."""
        self.dummy_request = Request()
        helpers.ALLOWED_HOSTS = [".dev-faq.com"]

    def test_subdomain(self):
        """Test ensuring get_subdomain returns the correct subdomain."""
        host_details = [
            {
                "scheme": "http",
                "host": "python.dev-faq.com",
                "expected_subdomain": "python",
                "expected_hostname": "dev-faq.com",
                "expected_port": 80,
                "expected_full_url": "http://python.dev-faq.com",
            },
            {
                "scheme": "http",
                "host": "python.dev-faq.com:8080",
                "expected_subdomain": "python",
                "expected_hostname": "dev-faq.com",
                "expected_port": 8080,
                "expected_full_url": "http://python.dev-faq.com:8080",
            },
            {
                "scheme": "http",
                "host": "php.dev-faq.com",
                "expected_subdomain": "php",
                "expected_hostname": "dev-faq.com",
                "expected_port": 80,
                "expected_full_url": "http://php.dev-faq.com",
            },
            {
                "scheme": "http",
                "host": "php.dev-faq.com",
                "expected_subdomain": "php",
                "expected_hostname": "dev-faq.com",
                "expected_port": 80,
                "expected_full_url": "http://php.dev-faq.com",
            },
            {
                "scheme": "http",
                "host": "dev-faq.com:8080",
                "expected_subdomain": "",
                "expected_hostname": "dev-faq.com",
                "expected_port": 8080,
                "expected_full_url": "http://dev-faq.com:8080",
            },
            {
                "scheme": "http",
                "host": "127.0.0.1",
                "expected_subdomain": "",
                "expected_hostname": "127.0.0.1",
                "expected_port": 80,
                "expected_full_url": "http://127.0.0.1",
            },
            {
                "scheme": "https",
                "host": "127.0.0.1:8080",
                "expected_subdomain": "",
                "expected_hostname": "127.0.0.1",
                "expected_port": 8080,
                "expected_full_url": "https://127.0.0.1:8080",
            },
            {
                "scheme": "https",
                "host": "other.domain.com",
                "expected_subdomain": "",
                "expected_hostname": "other.domain.com",
                "expected_port": 443,
                "expected_full_url": "https://other.domain.com",
            },
            {
                "scheme": "https",
                "host": "other.domain.com:8080",
                "expected_subdomain": "",
                "expected_hostname": "other.domain.com",
                "expected_port": 8080,
                "expected_full_url": "https://other.domain.com:8080",
            },
            {
                "scheme": "https",
                "host": "domain.com:8080",
                "expected_subdomain": "",
                "expected_hostname": "domain.com",
                "expected_port": 8080,
                "expected_full_url": "https://domain.com:8080",
            },
            {
                "scheme": "https",
                "host": "domain.com",
                "expected_subdomain": "",
                "expected_hostname": "domain.com",
                "expected_port": 443,
                "expected_full_url": "https://domain.com",
            },
            {
                "scheme": "https",
                "host": "domain",
                "expected_subdomain": "",
                "expected_hostname": "domain",
                "expected_port": 443,
                "expected_full_url": "https://domain",
            },
        ]

        for host_detail in host_details:
            self.dummy_request.META["HTTP_HOST"] = host_detail["host"]
            self.dummy_request.scheme = host_detail["scheme"]
            calculated_host_details: helpers.HostDetails = helpers.get_host_details(
                request=self.dummy_request
            )
            self.assertEqual(calculated_host_details.scheme, host_detail["scheme"])
            self.assertEqual(
                calculated_host_details.subdomain, host_detail["expected_subdomain"]
            )
            self.assertEqual(
                calculated_host_details.hostname, host_detail["expected_hostname"]
            )
            self.assertEqual(
                calculated_host_details.full_url, host_detail["expected_full_url"]
            )
            self.assertEqual(calculated_host_details.port, host_detail["expected_port"])
