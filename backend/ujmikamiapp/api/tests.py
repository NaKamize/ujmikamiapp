from django.test import TestCase
from rest_framework.test import APIClient


class ApiRoutingTestCase(TestCase):
    """api/urls.py only wires up sub-app routes; this checks that wiring resolves,
    not the business logic behind each endpoint (covered in projects/ml_models tests)."""

    def setUp(self):
        self.client = APIClient()

    def test_all_registered_endpoints_resolve(self):
        endpoints = [
            '/api/projects/',
            '/api/ml-models/',
            '/api/publications/',
            '/api/experiences/',
            '/api/about/',
        ]
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code, 200,
                f'{endpoint} returned {response.status_code}, expected 200'
            )

    def test_unknown_endpoint_returns_404(self):
        response = self.client.get('/api/does-not-exist/')
        self.assertEqual(response.status_code, 404)
