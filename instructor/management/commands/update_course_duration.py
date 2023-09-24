from django.core.management.base import BaseCommand
from django.db import models

from instructor.models import Course, Video


class Command(BaseCommand):
    help = 'Update course durations based on existing videos'

    def handle(self, *args, **kwargs):
        courses = Course.objects.all()

        for course in courses:
            total_duration = course.video_set.aggregate(
                total_duration=models.Sum('time_duration'))['total_duration']

            if total_duration is not None:
                course.course_duration = total_duration
                course.save()
            else:
                course.course_duration = 0
                course.save()

        self.stdout.write(self.style.SUCCESS(
            'Course durations updated successfully.'))
