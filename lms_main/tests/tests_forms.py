from django.test import TestCase
from lms_main.forms import AddCourseForm

from user.models import User,Instructor,Student
from lms_main.models import Course,Level
from instructor.models import Category

from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile

class AddCourseFormTests(TestCase):
    """Tests class for the Add Course Form"""

    def setUp(self):
        self.user = User.objects.create(
            first_name='instructor_user', last_name='lastname', email='instructor@gmail.com', password='abcde12345')
        self.instructor = Instructor.objects.create(instructor=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.level = Level.objects.create(name_of_level='Test Level')

    def test_valid_form(self):
        # Create a SimpleUploadedFile instance to simulate file upload
        image_data = b'fake image data'
        image = SimpleUploadedFile(
            "test_image.jpg", image_data, content_type="image/jpeg")

        form_data = {
            'title': 'Test Course',
            'description': 'This is a test course description.',
            'created_at': datetime.now(),
            'price': 100,
            'discount': 10,
            'slug': 'test-course',
            'status': 'PUBLISH',
            'author': self.instructor,  
            'category': self.category,  
            'level': self.level,  
        }

        form_files = {'featured_image': image}  # Attach the image to the form

        form = AddCourseForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {}  # Empty data intentionally to trigger validation errors

        form = AddCourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        # Number of expected validation errors
        # self.assertEqual(len(form.errors), 11)



