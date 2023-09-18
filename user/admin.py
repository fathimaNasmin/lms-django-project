from django.contrib import admin
from . import models
from student.models import EnrolledCourses


# admin.site.register(models.User)
admin.site.register(models.Student)
admin.site.register(models.Instructor)
admin.site.register(EnrolledCourses)
