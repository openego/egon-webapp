from django.test import TestCase


# Simple tests on project level
class HomepageUrlTests(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get("/")
        assert response.status_code == 200
