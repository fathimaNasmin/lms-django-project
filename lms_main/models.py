from . import models as lms_main_model
from user import models as user_model
from django.db import models
from PIL import Image
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

from .utils import slugify_course_instance_title, calculate_video_duration


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
    price = models.IntegerField(
        null=True, default=0)
    discount = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True,
                            blank=True, max_length=300)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    author = models.ForeignKey(user_model.Instructor, on_delete=models.CASCADE)
    category = models.ForeignKey(
        lms_main_model.Category, on_delete=models.CASCADE)
    level = models.ForeignKey(lms_main_model.Level, on_delete=models.CASCADE)

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

        # if self.slug is None:
        #     self.slug = slugify(self.title)
        #     self.save()


def course_slug_pre_save(sender, instance, *args, **kwargs):
    # print('pre_save')
    if instance.slug is None:
        slugify_course_instance_title(instance, save=False)


pre_save.connect(course_slug_pre_save, sender=Course)


def course_slug_post_save(sender, instance, created, *args, **kwargs):
    # print('post_save')
    if created:
        slugify_course_instance_title(instance, save=True)


post_save.connect(course_slug_post_save, sender=Course)


class Requirement(models.Model):
    """requirement of each course"""
    requirement_points = models.CharField(
        max_length=500, default="no requirements")

    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        lms_main_model.Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Requirement {self.requirement_points}"


class WhatYouWillLearn(models.Model):
    """what you'll learn of each course"""
    points = models.CharField(
        max_length=500, default="no points")

    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        lms_main_model.Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"What you'll Learn {self.points}"


class Lesson(models.Model):
    """lesson for each course"""
    name = models.CharField(
        max_length=200)

    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        lms_main_model.Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Lesson - {self.name} - {self.course.title}"


class Video(models.Model):
    """videos of each courses"""
    serial_number = models.IntegerField(null=True)
    title = models.CharField(
        max_length=100)
    youtube_id = models.CharField(
        max_length=200, unique=True)
    time_duration = models.FloatField(null=True, blank=True)

    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        lms_main_model.Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(
        lms_main_model.Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f"Video - {self.course.title}-{self.lesson.name}:-{self.title}"

    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        duration = calculate_video_duration(self.youtube_id)

        if duration:
            self.time_duration = duration

        super(Video, self).save()


class Cart(models.Model):
    """model to store the courses added to cart"""
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE)
    student = models.ForeignKey(
        user_model.Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.course.title}"

    class Meta:
        # Ensure that each combination of course and student is unique
        unique_together = ('course', 'student')


class SaveForLater(models.Model):
    """model for save for later feature"""
    saved_at = models.DateTimeField(auto_now_add=True)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE)
    student = models.ForeignKey(
        user_model.Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title}"

    class Meta:
        # Ensure that each combination of course and student is unique
        unique_together = ('course', 'student')

# Order model to store details of order


class Order(models.Model):
    """model to store details of order"""
    order_no = models.CharField(max_length=200, default=0, unique=True)
    total_price = models.IntegerField(null=True, default=0)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    student = models.ForeignKey(
        user_model.Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order No:{self.order_no}"

# OrderItems model to store items in the order


class OrderItems(models.Model):
    """model for storing items in the order"""

    item_price = models.IntegerField(null=True, default=0)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order Item by {self.order.student}-{self.course} in the {self.order}"

    class Meta:
        # Ensure that each combination of course and student is unique
        unique_together = ('course', 'order')
