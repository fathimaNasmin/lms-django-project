from django.test import SimpleTestCase
from django.urls import reverse 


class HomepageViewTests(SimpleTestCase):

    def test_home_page_view(self):
        """Test function to check url availbale by name"""
        response = self.client.get(reverse('lms_main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lms_main/home.html")
        self.assertContains(response, "<h5>Featured Teachers</h5>")
        self.assertNotContains(response, "Not on the page")

        