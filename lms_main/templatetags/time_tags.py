from django import template
from datetime import timedelta

register = template.Library()


@register.simple_tag
def time_in_hrs_min_sec(time_in_sec):
    return str(timedelta(seconds=time_in_sec))
