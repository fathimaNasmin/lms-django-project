from django.db.models.signals import pre_save, post_save,pre_delete
from django.dispatch import receiver

from .models import Course,Video

# signals for slug field of course
def course_slug_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_course_instance_title(instance, save=False)


pre_save.connect(course_slug_pre_save, sender=Course)


def course_slug_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_course_instance_title(instance, save=True)


post_save.connect(course_slug_post_save, sender=Course)


# post_save Signal for saving course-duration in Course model when uploading a new video
@receiver(post_save, sender=Video)
def update_course_duration(sender,instance, created, **kwargs):
    if created:
        course = instance.course
        total_duration = course.video_set.aggregate(
            total_duration=models.Sum('time_duration'))['total_duration']
        print(total_duration)
        if total_duration is not None:
            course.course_duration = total_duration
            course.save()
        else:
            course.course_duration = 0
            course.save()

# signal handler is triggered just before a Video object is deleted
@receiver(pre_delete, sender=Video)
def update_course_duration_on_video_delete(sender, instance, **kwargs):
    course = instance.course
    total_duration = course.video_set.exclude(pk=instance.pk).aggregate(
        total_duration=models.Sum('time_duration'))['total_duration']

    if total_duration is not None:
        course.course_duration = total_duration
        course.save()
    else:
        course.course_duration = 0
        course.save()
