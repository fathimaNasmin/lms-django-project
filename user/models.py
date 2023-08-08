# TODO: Student fields:first name;last name;email;password
#TODO: Instructor Model
#TODO: one-one field to instructor and student by adding additional fields

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(_("Username"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = instance.email

pre_save.connect(set_username, sender=User)


class Student(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,
    )

    def __str__(self):
        return f"Student {self.student.email}"


class Instructor(models.Model):
    instructor = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)

    def __str__(self):
        return f"Instructor {self.instructor.first_name}"