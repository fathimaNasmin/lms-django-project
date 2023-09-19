# importing models 
from . import models as lms_main_model
from user import models as user_model
from student.models import Order
from instructor.models import Category,Level,Requirement,WhatYouWillLearn,Lesson,Course

from django.db import models
from PIL import Image
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.core.validators import FileExtensionValidator

from .utils import slugify_course_instance_title, calculate_video_duration



# class Course(models.Model):
#     """Model to store courses"""
#     STATUS = (
#         ('PUBLISH', 'PUBLISH'),
#         ('DRAFT', 'DRAFT'),
#     )

#     title = models.CharField(max_length=300)
#     description = models.TextField()
#     created_at = models.DateField(auto_now_add=True)
#     featured_image = models.ImageField(
#         upload_to='course/featured_images/', null=True, blank=True)
#     # featured_video = models.CharField(max_length=500)
#     price = models.IntegerField(
#         null=True, default=0, blank=True)
#     discount = models.IntegerField(null=True, blank=True)
#     slug = models.SlugField(unique=True, null=True,
#                             blank=True, max_length=300)
#     status = models.CharField(choices=STATUS, max_length=100, null=True)
#     # ========FOREIGN KEY AND RELATIONSHIPS=======#
#     author = models.ForeignKey(user_model.Instructor, on_delete=models.CASCADE)
#     category = models.ForeignKey(
#         Category, on_delete=models.CASCADE)
#     level = models.ForeignKey(Level, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Course {self.title}"
    
#     @property
#     def featured_image_url(self):
#         if self.featured_image and hasattr(self.featured_image, 'url'):
#             return self.featured_image.url
#         else:
#             return "/static/images/no_image/No-image-found.jpg"

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         if self.featured_image:
#             img = Image.open(self.featured_image.path)
#             width, height = img.size

#             desired_width = 300  # Your desired width
#             desired_height = 300  # Your desired height

#             if width > desired_width or height > desired_height:
#                 img.thumbnail((desired_width, desired_height))
#                 img.save(self.featured_image.path)
#                 self.featured_image_width = img.width
#                 self.featured_image_height = img.height
#                 self.save()


# def course_slug_pre_save(sender, instance, *args, **kwargs):
#     if instance.slug is None:
#         slugify_course_instance_title(instance, save=False)


# pre_save.connect(course_slug_pre_save, sender=Course)


# def course_slug_post_save(sender, instance, created, *args, **kwargs):
#     if created:
#         slugify_course_instance_title(instance, save=True)


# post_save.connect(course_slug_post_save, sender=Course)



# class Video(models.Model):
#     """videos of each courses"""
#     title = models.CharField(
#         max_length=100)
#     video_file = models.FileField(upload_to='videos/', null=True, blank=True,
#                                   validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
#     time_duration = models.FloatField(null=True, blank=True)
#     upload_date = models.DateTimeField(auto_now_add=True)

#     # ========FOREIGN KEY AND RELATIONSHIPS=======#
#     course = models.ForeignKey(
#         Course, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(
#         Lesson, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Video - {self.course.title}-{self.lesson.name}:-{self.title}"

#     def save(self, *args, **kwargs):
#         # super().save(*args, **kwargs)
#         # duration is saved in 'seconds'
#         if self.video_file.path:
#             duration = calculate_video_duration(self.video_file.path)
#             print(duration)

#         if duration:
#             self.time_duration = duration

#         super(Video, self).save()




# =================QUIZ MODELS================================

class Question(models.Model):
    """Question model to store questions for quiz"""
    question_text = models.CharField(max_length=300)
    # foreignkey and relationship
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.question_text}"
    
# model to store options for the quiz
class QuizOption(models.Model):
    """model to store options for the quiz"""
    option = models.CharField(max_length=200)
    is_answer = models.BooleanField(default=False,blank=True)
    # Foreign Key and Relationships
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Options-{self.question_id.question_text}"