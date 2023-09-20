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




