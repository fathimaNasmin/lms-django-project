from django.test import TestCase, Client
from user.forms import SignUpForm, LoginForm
from user.models import User, Student, Instructor
from django.core.exceptions import ValidationError



class SignUpFormTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def tests_form_valid_data(self):
        """test form with valid data"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = SignUpForm(data)
        self.assertTrue(form.is_valid())

    
    def tests_form_invalid_data(self):
        """test form with invalid data"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'testexample.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def tests_form_firstname_and_lastname_validation(self):
        """test form with invalid number of characters in firstname and lastname"""
        first_name_error = {
            'first_name': 'ab',
            'last_name': 'lastname',
            'email': 'testexample.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        last_name_error = {
            'first_name': 'first_name',
            'last_name': 'xy',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form1 = SignUpForm(first_name_error)
        form2 = SignUpForm(last_name_error)

        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())

        self.assertRaises(ValidationError, form1.clean)
        self.assertRaises(ValidationError, form2.clean)

        with self.assertRaisesMessage(
                ValidationError,
                'Firstname and Lastname must be at least 2 characters long.'
        ):
            form1.clean()
            form2.clean
        

    
    def tests_form_firstname_not_character(self):
        """test form firstname contains non-alphabetical letters"""
        data = {
            'first_name': '1234',
            'last_name': 'lastname',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError, form.clean)
        with self.assertRaisesMessage(
                ValidationError,
                'First name must contain only alphabets.'
        ):
            form.clean()


    def tests_form_lastname_not_character(self):
        """test form lastname contains non-alphabetical letters"""
        data = {
            'first_name': 'firstname',
            'last_name': '12',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError, form.clean)
        with self.assertRaisesMessage(
                ValidationError,
                'Last Name must contain only alphabets.'
        ):
            form.clean()


    def test_valid_email(self):
        """test valid email format"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = SignUpForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_format(self):
        """test invalid email format"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'invalid_email_format',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    
    def test_empty_email_field(self):
        """test empty email field"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
        
        
        
    #PasswordFieldValidation
    def tests_password1_and_password2_are_equal(self):
        """tests password1 and password2 are equal"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = SignUpForm(data)
        self.assertEqual(data['password1'], data['password2'])

    def tests_empty_password(self):
        """tests for empty password"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'test@example.com',
            'password1': '',
            'password2': '',
        }

        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def tests_invalid_password_format(self):
        """tests password is commonly used"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'test@example.com',
            'password1': 'abc123',
            'password2': 'abc123',
        }

        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def tests_invalid_password_length(self):
        """test password is short"""
        data = {
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'test@example.com',
            'password1': 'abc123',
            'password2': 'abc123',
        }

        form = SignUpForm(data)
        self.assertFalse(form.is_valid())


class LoginFormTest(TestCase):
    """Test class for Login Form"""

    def setUp(self):
        self.client = Client()
        self.new_user = User(first_name='user first name',
            last_name= 'user last name',
            email='abcde@gmail.com')
        self.new_user.set_password('jnsjdhjHGShbd128')
        self.new_user.save()
        self.new_student = Student(student_id=self.new_user.id)
        self.new_student.save()


    def tests_form_with_valid_data(self):
        data = {
            'username':'abcde@gmail.com',
            'password' : 'jnsjdhjHGShbd128'
        }

        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())


    def tests_form_with_incorrect_password(self):
        data = {
            'username':'abcde@gmail.com',
            'password' : 'jnsjdhjHd128'
        }

        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Incorrect email or password', form.errors['__all__'])

    
    def test_non_existent_user(self):
        form_data = {'username': 'nonexistent@example.com', 'password': 'testpassword'}
        form = LoginForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("Student doesn't exists", form.errors['__all__'])



