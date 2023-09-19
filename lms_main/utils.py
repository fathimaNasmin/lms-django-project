import os
import requests
import re
from random import randint
from dotenv import load_dotenv
from datetime import timedelta
from django.utils.text import slugify
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files import File
import time
from moviepy.video.io.VideoFileClip import VideoFileClip

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def slugify_course_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        rand_int = randint(300_000, 500_000)
        slug = f"{slug}-{rand_int}"
        return slugify_course_instance_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance



def calculate_video_duration(video_path):
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.close()  # Close the video file
        duration = round(duration,2)
        return duration
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# function to generate Receipt using xhtml2pdf
def receipt_render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return None
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")),
                   dest=result, encoding='UTF-8')

    # Create a File object from the PDF content
    order_no = context_dict['order']
    print(order_no)
    print(context_dict)
    pdf_name = f'{order_no}.pdf'
    result.seek(0)
    pdf_file_object = File(result, name=pdf_name)
    return pdf_file_object
    # return None


def generate_order_number():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    invoice_number = f"{timestamp}#{randint(1, 99999)}"
    return invoice_number
