from django.test import TestCase
from user.models import User, Student, Instructor


class UserModelTest(TestCase):

    def tests_create_new_user(self):
        """test function to test creation of new user"""
        new_user = User(first_name='user first name',
            last_name= 'user last name',
            email='abcde@gmail.com')
        new_user.set_password('jnsjdhjHGShbd128')
        new_user.save()

        user_from_db = User.objects.get(id=new_user.id)

        self.assertEqual(new_user.first_name,'user first name')
        self.assertEqual(new_user.last_name,'user last name')
        self.assertEqual(new_user.email,'abcde@gmail.com')
        self.assertEqual(str(new_user), 'abcde@gmail.com')

    def tests_create_new_Student(self):
        """tests function to test creation of new student user"""
        new_user = User(first_name='user first name',
            last_name= 'user last name',
            email='abcde@gmail.com')
        new_user.set_password('jnsjdhjHGShbd128')
        new_user.save()
        new_student = Student(student_id=new_user.id)
        new_student.save()

        # retriving data from db
        student_obj = User.objects.get(id=new_user.id)
        self.assertEqual(student_obj.email, 'abcde@gmail.com')


    def tests_create_new_Student(self):
        """tests function to test creation of new instructor user"""
        new_user = User(first_name='user first name',
            last_name= 'user last name',
            email='abcde@gmail.com')
        new_user.set_password('jnsjdhjHGShbd128')
        new_user.save()
        new_instructor = Instructor(instructor_id=new_user.id)
        new_instructor.save()

        # retriving data from db
        instructor_obj = User.objects.get(id=new_user.id)
        self.assertEqual(instructor_obj.email, 'abcde@gmail.com')

    def tests_unique_email_address(self):
        """tests function to test unique constraint of email"""
        user1 = User(first_name='user1',
            last_name= 'user1',
            email='abcde@gmail.com')
        user1.set_password('jnsjd#$56bd128')

        user1.save()

        with self.assertRaises(Exception) as e:
            user2 = User(first_name='user2',
            last_name= 'user2',
            email='abcde@gmail.com')
            user2.set_password('jnsjdhjHGShbd128')
            user2.save()
            self.assertEqual(IntegrityError, type(e.Exception))