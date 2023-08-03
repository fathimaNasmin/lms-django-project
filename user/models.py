# TODO: Student fields:first name;last name;email;password
#TODO: Instructor Model
#TODO: one-one field to instructor and student by adding additional fields

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Student(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,
    )

    def __str__(self):
        return f"Student {self.user.email}"


class Instructor(models.Model):
    instructor = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)

    def __str__(self):
        return f"Instructor {self.instructor.first_name}"