from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render, redirect
from django.db import IntegrityError
from . import models
from user import models as user_model
from django.db.models import Sum
from lms_main.templatetags import course_tags


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
    print(user.is_authenticated)
    context = {
        'course': single_course,
        'videos': videos,
        'total_time_duration_course': total_time_duration_course,
        'no_of_videos': videos.count(),
    }
    if user.is_authenticated:
        user_enrolled_course = user_model.EnrolledCourses.objects.filter(
            course=single_course, student=user.student).exists()
        course_exists_in_cart = models.AddToCart.objects.filter(
            course=single_course, student=user.student).exists()
        print("user_enrolled_course:", user_enrolled_course)
        print("course_exists_in_cart:", course_exists_in_cart)
        context['user_enrolled_course'] = user_enrolled_course
        context['course_exists_in_cart'] = course_exists_in_cart

    # print(context)
    return render(request, 'lms_main/single_course.html', context)


@login_required(login_url='/user/login/')
def enroll_course(request, slug):
    """view to enroll the course for logged in students"""
    user = request.user
    # print(user)
    course = models.Course.objects.filter(slug=slug).first()
    # print(f"from enrolled page{course}")
    data = {}

    if request.method == 'POST' and request.is_ajax():

        try:
            student_course_enroll = user_model.EnrolledCourses(
                course=course, student=request.user.student
            )
            student_course_enroll.save()
            # print(f"{user} enrolled for the course-{slug}")
            data['success'] = True
            # print(f"json_data{data}")
        except Exception as e:
            print(f"error:{e}")
        return HttpResponse(json.dumps(data), content_type='application/json')
    return redirect('lms_main:single-course', slug)


@login_required(login_url='/user/login/')
def add_to_cart(request, slug):
    """view to add the courses to cart to purchase"""
    user = request.user
    # print(user)
    course = models.Course.objects.filter(slug=slug).first()
    print(f"from add to cart page:{course}", sep="\n")
    data = {}
    course_exists_in_cart = models.AddToCart.objects.filter(
        course=course, student=user.student).exists()
# ifuser is authenticated
    if not course_exists_in_cart:
        if request.method == 'POST' and request.is_ajax():
            try:
                added_to_cart = models.AddToCart(
                    course=course, student=request.user.student
                )
                added_to_cart.save()
                # print(f"{user} enrolled for the course-{slug}")
                data['success'] = True
                # print(f"json_data{data}")
            except IntegrityError as e:
                print(e)
                data['success'] = False
            except Exception as e:
                print(f"error:{e}")
                data['success'] = False

            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return redirect('lms_main:single-course', slug)

    return redirect('lms_main:single-course', slug)


@login_required
def go_to_cart(request):
    """Shopping cart shows all the courses added to the user cart"""
    price = []
    discount = []
    user = request.user
    user_cart_items = models.AddToCart.objects.filter(student=user.student)
    # total_price = sum([item.course.price for item in user_cart_items])
    # discount_price =
    # print(total_price)
    for item in user_cart_items:
        price.append(item.course.price)
        discount.append(course_tags.discount_calculation(
            item.course.price, item.course.discount))
    total_price = sum(price)
    discount = sum(discount)
    total_discount = total_price - discount
    amount_to_pay = total_price - discount
    context = {
        'items_in_cart': user_cart_items,
        'total_price': total_price,
        'total_discount': total_discount,
        'amount_to_pay': amount_to_pay,
    }
    print(context)
    return render(request, 'lms_main/shopping_cart.html', context)
