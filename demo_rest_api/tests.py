from django.test import SimpleTestCase
from django.urls import reverse


class DemoRestApiViewsTest(SimpleTestCase):
    def test_index_view_returns_ok(self):
        response = self.client.get(reverse("demo_rest_api:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "demo_rest_api")
