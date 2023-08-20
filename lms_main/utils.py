import requests
from datetime import timedelta
import re
from django.utils.text import slugify
import random


def slugify_course_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        rand_int = random.randint(300_000, 500_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def calculate_video_duration(id):
    """calculate the video duration using Google API"""
    video_id = id
    url = f"https://www.googleapis.com/youtube/v3/videos?key=AIzaSyB_hnKQO4oO0WY7rJ_1eV6ifHBqLcA7d9A&part=contentDetails&id={video_id}"

    payload = {}
    headers = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()

            duration = data['items'][0]['contentDetails']['duration']

            # get the duration in seconds using regular expression
            hours_pattern = re.compile(r'(\d+)H')
            minutes_pattern = re.compile(r'(\d+)M')
            seconds_pattern = re.compile(r'(\d+)S')

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            # print(hours, minutes, seconds)

            video_duration = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            return video_duration
        else:
            return 0
    except requests.RequestException as e:
        print(f"Error while fetching video duration: {e}")
        return 0
