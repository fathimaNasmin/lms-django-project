from django.test import SimpleTestCase,TestCase
from django.urls import reverse,resolve



class HomepageUrlTests(TestCase):
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

# Instructor Page Testing

class InstructorSignUpPageTest(TestCase):
    """tests the instructor signup page """
    def tests_signup_url_correct_location(self):
        response = self.client.get(reverse('lms_main:instructor-signup'))
        self.assertEqual(response.status_code, 200)

    def tests_signup_url_locate_by_name(self):
        response = self.client.get('/instructor/instructor-signup/')
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        """Test Function to check template name correct"""
        response = self.client.get(reverse("lms_main:instructor-signup"))
        self.assertTemplateUsed(response, "user/instructor/instructor_signup.html")

    
    def test_template_content(self):
        """Test Function for template content"""
        response = self.client.get(reverse("lms_main:instructor-signup"))
        self.assertContains(response, "<h4>Signup and start teaching</h4>")
        self.assertNotContains(response, "Not on the page")
    


class InstructorLoginPageTest(TestCase):
    """Test class to test the url of Instructor's login page"""

    def tests_instructor_login_url_exists_at_correct_location(self):
        response = self.client.get('/instructor/instructor-login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("lms_main:instructor-login"))
        self.assertEqual(response.status_code, 200)

    def test_login_template_name_correct(self):  
        """Test Function to check template name correct"""
        response = self.client.get(reverse("lms_main:instructor-login"))
        self.assertTemplateUsed(response, "user/instructor/instructor_login.html")

    
    def test_template_content(self):
        """Test Function for template content"""
        response = self.client.get(reverse("lms_main:instructor-login"))
        self.assertContains(response, "<h4>Log in to your Edubin Instructor account</h4>")
        self.assertNotContains(response, "Not on the page")

        
class InstructorDashboardPageTest(TestCase):
    """Test class to test the url of dashboard page"""

    def tests_login_url_exists_at_correct_location(self):
        response = self.client.get('/instructor/instructor-dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("lms_main:instructor-dashboard"))
        self.assertEqual(response.status_code, 302)


class InstructorLogoutPageTest(TestCase):
    """Test class to test the url of logout page"""

    def tests_login_url_exists_at_correct_location(self):
        response = self.client.get('/instructor/instructor-logout/')
        self.assertEqual(response.status_code, 302)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("lms_main:instructor-logout"))
        self.assertEqual(response.status_code, 302)
        