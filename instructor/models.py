from django.db import models

from django.utils.text import slugify
from PIL import Image

from django.db.models.signals import pre_save, post_save




class Category(models.Model):
    """Model to store category of course"""
    name = models.CharField(max_length=80)
    icon = models.ImageField(null=True, blank=True,
                             upload_to='icons/category/')
    slug = models.SlugField(unique=True, null=True,
                            blank=True, max_length=300)

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

        # slugify the title of category
        if self.slug is None:
            self.slug = slugify(f"category{self.name}{self.id}")
            self.save()


class Level(models.Model):
    """Level of each course"""
    name_of_level = models.CharField(
        max_length=30, null=True, blank=True, default=None)

    def __str__(self):
        return f"Level {self.name_of_level}"


class Requirement(models.Model):
    """requirement of each course"""
    requirement_points = models.CharField(
        max_length=500, default="")

    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)

    def __str__(self):
        return f"Requirement {self.requirement_points}"


class WhatYouWillLearn(models.Model):
    """what you'll learn of each course"""
    points = models.CharField(
        max_length=500, default="no points")

    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)

    def __str__(self):
        return f"What you'll Learn {self.points}"


class Lesson(models.Model):
    """lesson for each course"""
    name = models.CharField(
        max_length=200)

    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)

    def __str__(self):
        return f"Lesson - {self.name} - {self.course.title}"


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
        upload_to='course/featured_images/', null=True, blank=True)
    # featured_video = models.CharField(max_length=500)
    price = models.IntegerField(
        null=True, default=0, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True,
                            blank=True, max_length=300)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    author = models.ForeignKey("user.Instructor", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return f"Course {self.title}"

    @property
    def featured_image_url(self):
        if self.featured_image and hasattr(self.featured_image, 'url'):
            return self.featured_image.url
        else:
            return "/static/images/no_image/No-image-found.jpg"

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


def course_slug_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_course_instance_title(instance, save=False)


pre_save.connect(course_slug_pre_save, sender=Course)


def course_slug_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_course_instance_title(instance, save=True)


post_save.connect(course_slug_post_save, sender=Course)
