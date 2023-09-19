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




# # =================QUIZ MODELS================================

# class Question(models.Model):
#     """Question model to store questions for quiz"""
#     question_text = models.CharField(max_length=300)
#     # foreignkey and relationship
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.question_text}"
    
# # model to store options for the quiz
# class QuizOption(models.Model):
#     """model to store options for the quiz"""
#     option = models.CharField(max_length=200)
#     is_answer = models.BooleanField(default=False,blank=True)
#     # Foreign Key and Relationships
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Options-{self.question_id.question_text}"