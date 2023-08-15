from django.shortcuts import render
from django.http import HttpResponse

from . import models

def home_page(request):
    categories = models.Category.objects.all()
    courses = models.Course.objects.filter(status='PUBLISH').all()
    print(courses)
    print(categories)

    context = {
        'categories': categories,
    }

    return render(request, 'lms_main/home.html', context)



def category_detail(request, id):
    """displays all the courses under the category"""
    category_obj = models.Category.objects.get(id=id)
    categories = models.Category.objects.all()
    category_courses = models.Course.objects.filter(status='PUBLISH',category_id=category_obj.id).all()

    # print(category_courses)
    # print(category_obj)

    context = {
        'categories': categories,
        'category_courses':category_courses,
        'category_obj':category_obj,
    }
    # for course in category_courses:
    #     print(course.author.instructor.last_name)
        

    return render(request, 'lms_main/category_detail.html', context)


def course_lists(request):
    """displays the course lists"""
    categories = models.Category.objects.all()
    all_courses = models.Course.objects.filter(status='PUBLISH').all()
    context = {
        'categories': categories,
        'courses': all_courses,
    }
    # for course in all_courses:
    #     print(course.author.instructor.first_name)
        

    return render(request, 'lms_main/course_lists.html', context)
