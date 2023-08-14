from django.shortcuts import render
from django.http import HttpResponse

from . import models

def home_page(request):
    categories = models.Category.objects.all()
    print(categories)

    context = {
        'categories': categories,
    }

    return render(request, 'lms_main/home.html', context)
