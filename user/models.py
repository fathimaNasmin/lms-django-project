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
    profile_image = models.ImageField(null=True, blank=True, upload_to="profile_pictures/student/")

    def __str__(self):
        return f"Student {self.student.email}"

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            width, height = img.size
            
            desired_width = 300  # Your desired width
            desired_height = 300  # Your desired height

            if width > desired_width or height > desired_height:
                img.thumbnail((desired_width, desired_height))
                img.save(self.profile_image.path)
                self.profile_image_width = img.width
                self.profile_image_height = img.height
                self.save()


class Instructor(models.Model):
    instructor = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profile_pictures/instructor/")

    def __str__(self):
        return f"Instructor {self.instructor.first_name}"