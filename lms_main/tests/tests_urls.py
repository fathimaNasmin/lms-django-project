from django.test import SimpleTestCase
from django.urls import reverse  


class HomepageUrlTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    
    def test_url_available_by_name(self):
        """Test function to check url availbale by name"""
        response = self.client.get(reverse('lms_main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lms_main/home.html")
        self.assertContains(response, "<h5>Featured Teachers</h5>")
        self.assertNotContains(response, "Not on the page")

        