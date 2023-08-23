from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render, redirect
from . import models
from user import models as user_model


def home_page(request):
    categories = models.Category.objects.all()
    courses = models.Course.objects.filter(status='PUBLISH').all()
    # print(courses)
    # print(categories)

    context = {
        'categories': categories,
    }

    return render(request, 'lms_main/home.html', context)


def search(request):
    query = request.GET.get('query')
    search_results = models.Course.objects.filter(title__icontains=query).all()
    # print(courses)

    context = {
        'search_results': search_results,
    }

    return render(request, 'lms_main/search.html', context)

    # return JsonResponse({"message": "message for search view",
    #                      'query_result': courses})


def category_detail(request, slug):
    """displays all the courses under the category"""
    print(slug)
    category_obj = models.Category.objects.filter(slug=slug).first()
    print(category_obj)
    categories = models.Category.objects.all()
    category_courses = models.Course.objects.filter(
        status='PUBLISH', category_id=category_obj.id).all()

    # print(category_courses)
    # print(category_obj)

    context = {
        'categories': categories,
        'category_courses': category_courses,
        'category_obj': category_obj,
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


def single_course(request, slug):
    """view for single course in detail"""
    single_course = models.Course.objects.filter(slug=slug).first()
    videos = models.Video.objects.filter(course__slug=slug)
    total_time_duration_course = sum([video.time_duration for video in videos])
    context = {}
    user = request.user

    if user.is_authenticated:
        user_enrolled_course = user_model.EnrolledCourses.objects.filter(
            course=single_course, student=user.student).exists()
        print(user_enrolled_course)
        context['user_enrolled_course'] = user_enrolled_course

    context = {
        'course': single_course,
        'videos': videos,
        'total_time_duration_course': total_time_duration_course,
        'no_of_videos': videos.count(),
    }

    return render(request, 'lms_main/single_course.html', context)


@login_required(login_url='/user/login/')
def enroll_course(request, slug):
    """view to enroll the course for logged in students"""
    user = request.user
    print(user)
    course = models.Course.objects.filter(slug=slug).first()
    print(f"from enrolled page{course}")
    data = {}

    if request.method == 'POST' and request.is_ajax():

        try:
            student_course_enroll = user_model.EnrolledCourses(
                course=course, student=request.user.student
            )
            student_course_enroll.save()
            print(f"{user} enrolled for the course-{slug}")
            data['success'] = True
            print(f"json_data{data}")
        except Exception as e:
            print(f"error:{e}")
        return HttpResponse(json.dumps(data), content_type='application/json')
    return redirect('lms_main:single-course', slug)
