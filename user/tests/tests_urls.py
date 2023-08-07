from django.test import TestCase
from django.urls import reverse,resolve



class SignUpPageTest(TestCase):
    """Test Class to test Sign Up page"""
    
    def test_url_exists_at_correct_location(self):
        """function to test url exists at correct location or not"""
        response = self.client.get('/user/signup/')
        self.assertEqual(response.status_code, 200)

    
    def test_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("user:signup"))
        self.assertEqual(response.status_code, 200)

    
    def test_template_name_correct(self):  
        """Test Function to check template name correct"""
        response = self.client.get(reverse("user:signup"))
        self.assertTemplateUsed(response, "user/signup.html")

    
    def test_template_content(self):
        """Test Function for template content"""
        response = self.client.get(reverse("user:signup"))
        self.assertContains(response, "<h4>Signup and start learning</h4>")
        self.assertNotContains(response, "Not on the page")
        

    


    