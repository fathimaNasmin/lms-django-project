from django.test import SimpleTestCase,TestCase, Client
from django.urls import reverse

import json
from user.models import Student, User, Instructor
from user.forms import SignUpForm 


class HomepageViewTests(TestCase):

    def test_home_page_view(self):
        """Test function to check url availbale by name"""
        response = self.client.get(reverse('lms_main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lms_main/home.html")
        self.assertContains(response, "<h5>Featured Teachers</h5>")
        self.assertNotContains(response, "Not on the page")

# Instructor View Page test

class InstructorSignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("lms_main:instructor-signup")
        

    def tests_signup_page_GET(self):
        """tests for signup page view"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/instructor/instructor_signup.html")
        self.assertContains(response, "<h4>Signup and start teaching</h4>")
        self.assertNotContains(response, "Not on the page")

    def tests_signup_success(self):
        # Simulate a valid AJAX POST request with form data
        data = {
            'first_name': 'testuser',
            'last_name': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('lms_main:instructor-signup'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Check if the response is a JSON response with success: True
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        response_data = response.json()
        self.assertTrue(response_data['success'])
        
        # Check if a new user and student were created
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())
        self.assertTrue(Instructor.objects.filter(instructor_id=response_data['new_instructor_id']).exists())


    def tests_signup_failure(self):
        """posting fail on invalid or missing data"""
        data = {
            'first_name': '',
            'last_name': 'sd',
            'email': 'testuserexample.com',
            'password1': 'testpassw',
            'password2': 'testpassword123',
        }
        response = self.client.post(self.signup_url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('email', response_data['errors']) 
        self.assertIn('password2', response_data['errors'])

        self.assertFalse(User.objects.filter(email='testuserexample.com').exists())
        self.assertFalse(Instructor.objects.filter(instructor_id=response_data['new_instructor_id']).exists())

class InstructorLoginViewTest(TestCase):
    """Test Class for Login View"""

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("lms_main:instructor-login")

    def tests_login_view_page_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/instructor/instructor_login.html')

    
    def test_login_success(self):
        #Create new user
        data = {
            'first_name': 'testuser',
            'last_name': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('lms_main:instructor-signup'), data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        data = {
            'username': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response_login = self.client.post(reverse('lms_main:instructor-login'), data=data,
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response_login.status_code, 200)
        self.assertEqual(response_login['content-type'], 'application/json')
        response_data = response_login.json()
        print(response_data)
        # self.assertTrue(response_data['success'])
        
        
class InstructorDashboardViewTest(TestCase):
    """Test Class for instructor dashboard View"""

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("lms_main:instructor-dashboard")

    def tests_dashboard_view_page_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(
            response, 'user/instructor/instructor_dashboard.html')

       