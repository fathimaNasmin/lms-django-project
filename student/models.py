from django.db import models
from user.models import Student

# Create your models here.


class EnrolledCourses(models.Model):
    """model for enrolled courses by students"""
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        "lms_main.Course", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Course Enrolled {self.course.title}-{self.student}"

    class Meta:
        # Ensure that each combination of course and student is unique
        unique_together = ('course', 'student')
