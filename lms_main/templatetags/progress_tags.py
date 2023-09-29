from django import template
import math

register = template.Library()


@register.simple_tag
def progress_percentage(watched_duration, total_course_duration):
    if total_course_duration == 0.0 or watched_duration == 0.0:
        return 0
    else:
        percentage = (watched_duration / total_course_duration) * 100
        # print(percentage)
        # print(math.floor(percentage))
        return math.floor(percentage)
