from django.db import models
from PIL import Image

from user import models as user_model
from . import models as lms_main_model


class Category(models.Model):
    """Model to store category of course"""
    name = models.CharField(max_length=80)
    icon = models.ImageField(null=True, blank=True,
                             upload_to='icons/category/')

    def __str__(self):
        return f"Category {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.icon:
            img = Image.open(self.icon.path)
            width, height = img.size

            desired_width = 300  # Your desired width
            desired_height = 300  # Your desired height

            if width > desired_width or height > desired_height:
                img.thumbnail((desired_width, desired_height))
                img.save(self.icon.path)
                self.icon_width = img.width
                self.icon_height = img.height
                self.save()


class Level(models.Model):
    """Level of each course"""
    name_of_level = models.CharField(
        max_length=30, null=True, blank=True)

    def __str__(self):
        return f"Level {self.name_of_level}"


class Course(models.Model):
    """Model to store courses"""
    STATUS = (
        ('PUBLISH', 'PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    title = models.CharField(max_length=300)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    featured_image = models.ImageField(
        upload_to='course/featured_images/', null=True)
    # featured_video = models.CharField(max_length=500)
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(default='', max_length=400, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    author = models.ForeignKey(user_model.Instructor, on_delete=models.CASCADE)
    category = models.ForeignKey(
        lms_main_model.Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Course {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.featured_image:
            img = Image.open(self.featured_image.path)
            width, height = img.size

            desired_width = 300  # Your desired width
            desired_height = 300  # Your desired height

            if width > desired_width or height > desired_height:
                img.thumbnail((desired_width, desired_height))
                img.save(self.featured_image.path)
                self.featured_image_width = img.width
                self.featured_image_height = img.height
                self.save()
