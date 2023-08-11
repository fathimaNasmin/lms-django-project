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


class LoginPageTest(TestCase):
    """Test class to test the url of login page"""

    def tests__url_exists_at_correct_location(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("user:login-user"))
        self.assertEqual(response.status_code, 200)

    def test_login_template_name_correct(self):  
        """Test Function to check template name correct"""
        response = self.client.get(reverse("user:login-user"))
        self.assertTemplateUsed(response, "user/login.html")

    
    def test_template_content(self):
        """Test Function for template content"""
        response = self.client.get(reverse("user:login-user"))
        self.assertContains(response, "<h4>Log in to your Edubin account</h4>")
        self.assertNotContains(response, "Not on the page")

        
class DashboardPageTest(TestCase):
    """Test class to test the url of dashboard page"""

    def tests_login_url_exists_at_correct_location(self):
        response = self.client.get('/user/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("user:dashboard"))
        self.assertEqual(response.status_code, 302)


class LogoutPageTest(TestCase):
    """Test class to test the url of logout page"""

    def tests_login_url_exists_at_correct_location(self):
        response = self.client.get('/user/logout/')
        self.assertEqual(response.status_code, 302)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("user:logout-user"))
        self.assertEqual(response.status_code, 302)


# Instructor Page Testing

class InstructorSignUpPageTest(TestCase):
    """tests the instructor signup page """
    def tests_signup_url_correct_location(self):
        response = self.client.get(reverse('user:instructor-signup'))
        self.assertEqual(response.status_code, 200)

    def tests_signup_url_locate_by_name(self):
        response = self.client.get('/user/instructor-signup/')
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        """Test Function to check template name correct"""
        response = self.client.get(reverse("user:instructor-signup"))
        self.assertTemplateUsed(response, "user/instructor/instructor_signup.html")

    
    def test_template_content(self):
        """Test Function for template content"""
        response = self.client.get(reverse("user:instructor-signup"))
        self.assertContains(response, "<h4>Signup and start teaching</h4>")
        self.assertNotContains(response, "Not on the page")
    


class InstructorLoginPageTest(TestCase):
    """Test class to test the url of Instructor's login page"""

    def tests_instructor_login_url_exists_at_correct_location(self):
        response = self.client.get('/user/instructor-login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("user:instructor-login"))
        self.assertEqual(response.status_code, 200)

    def test_login_template_name_correct(self):  
        """Test Function to check template name correct"""
        response = self.client.get(reverse("user:instructor-login"))
        self.assertTemplateUsed(response, "user/instructor/instructor_login.html")

    
    def test_template_content(self):
        """Test Function for template content"""
        response = self.client.get(reverse("user:instructor-login"))
        self.assertContains(response, "<h4>Log in to your Edubin Instructor account</h4>")
        self.assertNotContains(response, "Not on the page")

        
class InstructorDashboardPageTest(TestCase):
    """Test class to test the url of dashboard page"""

    def tests_login_url_exists_at_correct_location(self):
        response = self.client.get('/user/instructor-dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("user:instructor-dashboard"))
        self.assertEqual(response.status_code, 302)


class InstructorLogoutPageTest(TestCase):
    """Test class to test the url of logout page"""

    def tests_login_url_exists_at_correct_location(self):
        response = self.client.get('/user/instructor-logout/')
        self.assertEqual(response.status_code, 302)

    def test_login_url_available_by_name(self):  
        """Test Function to check url available by name"""
        response = self.client.get(reverse("user:instructor-logout"))
        self.assertEqual(response.status_code, 302)