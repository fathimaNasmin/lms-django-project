from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
import math
import random
from django.shortcuts import render, redirect
from django.db import IntegrityError
from . import models
from user import models as user_model
from django.db.models import Sum
from lms_main.templatetags import course_tags, invoice
from .utils import receipt_render_to_pdf

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


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
            course=single_course, student=user.student)
        course_exists_in_cart = models.Cart.objects.filter(
            course=single_course, student=user.student)
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
    course_exists_in_cart = models.Cart.objects.filter(
        course=course, student=user.student).exists()
# ifuser is authenticated
    if not course_exists_in_cart:
        if request.method == 'POST' and request.is_ajax():
            try:
                added_to_cart = models.Cart(
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
def shopping_cart(request):
    """Shopping cart shows all the courses added to the user cart"""
    t_price = 0
    t_discount = 0

    current_user_items_list = []

    user = request.user
    user_cart_items = models.Cart.objects.filter(student=user.student)

    for item in user_cart_items:
        current_user_items_dict = {}
        current_user_items_dict['title'] = item.course.title
        current_user_items_dict['featured_image_url'] = item.course.featured_image.url
        current_user_items_dict['price'] = item.course.price
        current_user_items_dict['discount'] = item.course.discount

        current_user_items_list.append(current_user_items_dict)
        # calculate the total amount after discount
        t_price += item.course.price
        t_discount += course_tags.discount_calculation(
            item.course.price, item.course.discount)

    # create session to store current logged in user cart items
    request.session['current_user_items'] = current_user_items_list
    request.session['original_price'] = t_price
    request.session['discount_price'] = t_price - t_discount
    request.session['amount_to_pay'] = request.session['original_price'] - \
        request.session['discount_price']

    context = {
        'items_in_cart': request.session['current_user_items'],
        'total_price': request.session['original_price'],
        'total_discount': request.session['discount_price'],
        'amount_to_pay': request.session['amount_to_pay'],
    }
    # print(context)
    return render(request, 'lms_main/shopping_cart.html', context)

# View for to add course to 'save forlater'


@login_required
def save_for_later(request):
    """View for to add course to 'save forlater'"""
    user = request.user
    user_saved = models.SaveForLater.objects.filter(student=user.student)
    context = {
        'user_saved_courses': user_saved
    }
    data = {}

    if request.method == 'POST' and request.is_ajax():
        course = models.Course.objects.get(id=request.POST['course_id'])
        try:
            add_to_save_for_later = models.SaveForLater(
                course=course, student=user.student)
            remove_from_cart = models.Cart.objects.filter(
                course=course, student=user.student)
        except Exception as e:
            print(f"Error in try block:{e}")
            data['success'] = False
        else:
            add_to_save_for_later.save()
            remove_from_cart.delete()
        finally:
            data['success'] = True
            print("Exit from error handling")
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')
    print(f"context:{context}")
    return render(request, 'lms_main/save_for_later.html', context)


# view to add the courses from 'save for later' page to cart


@login_required(login_url='/user/login/')
def save_for_later_to_cart(request):
    """view to add the courses from 'save for later' page to cart """
    user = request.user
    course_id = request.POST['course_id']
    course = models.Course.objects.filter(id=course_id).first()
    data = {}

    course_exists_in_cart = models.Cart.objects.filter(
        course=course, student=user.student).exists()
    print("course exists", course_exists_in_cart)

    if not course_exists_in_cart:
        if request.method == 'POST' and request.is_ajax():
            try:
                remove_from_save_for_later = models.SaveForLater.objects.filter(
                    course=course, student=user.student).delete()

                add_to_cart = models.Cart(
                    course=course, student=user.student
                )
                add_to_cart.save()

                data['success'] = True

            except IntegrityError as e:
                print(e)
                data['success'] = False
            except Exception as e:
                print(f"error:{e}")
                data['success'] = False
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return redirect('lms_main:save-for-later')

    return redirect('lms_main:save-for-later')


# View function to remove course from shopping cart
@login_required(login_url='/user/login/')
def remove_from_cart(request):
    """View function to remove course from shopping cart"""
    user = request.user
    course_id = request.POST['course_id']
    # print(course_id)
    course = models.Course.objects.filter(id=course_id).first()
    # print(course)
    print(f"Item to remove:{course}", sep="\n")
    data = {}

    if request.method == 'POST' and request.is_ajax():
        try:
            remove_course_from_cart = models.Cart.objects.filter(
                course=course, student=user.student).delete()

            data['success'] = True

        except IntegrityError as e:
            print(e)
            data['success'] = False
        except Exception as e:
            print(f"error:{e}")
            data['success'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return redirect('lms_main:shopping-cart')

    return redirect('lms_main:shopping-cart')


# View function for the payment for course in the shopping cart


@login_required
@csrf_exempt
def checkout(request):
    """View function for the payment for course in the shopping cart"""
    user = request.user
    data = {}
    amount = request.session['amount_to_pay']

    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": f"Order-Id-{random.randint(1,100000)}",
        "invoice": f"INV-{random.randint(1,100000)}",
        "notify_url": request.build_absolute_uri(reverse('lms_main:paypal-ipn')),
        "return": request.build_absolute_uri(reverse('lms_main:payment-success')),
        "cancel_return": request.build_absolute_uri(reverse('lms_main:payment-failure')),

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        'items_in_cart': request.session['current_user_items'],
        'total_price': request.session['original_price'],
        'total_discount': request.session['discount_price'],
        'amount_to_pay': request.session['amount_to_pay'],
        'form': form,
    }

    if request.method == 'POST' and request.is_ajax():
        # Get the value from the POST data
        # total_amount = request.POST.get('amount_to_pay')
        # data["total_amount"] = total_amount
        return HttpResponse(json.dumps(data), content_type='application/json')
    # print(context)
    return render(request, 'lms_main/checkout.html', context)


@login_required
def payment_success_view(request):
    user = request.user
    context = {}
    if request.session['current_user_items']:

        # create order items
        try:
            # create order
            order = models.Order.objects.create(
                student=user.student,
                total_price=request.session['amount_to_pay'],
                paid_status=True,
                order_no=invoice.generate_order_number())
            for item in request.session['current_user_items']:

                course = models.Course.objects.filter(
                    title=item['title']).first()
                item_price = 0
                item_price = math.floor(item['price'] -
                                        item['price'] * item['discount'] / 100)
                # print(item_price)

                order_items = models.OrderItems.objects.create(
                    course=course,
                    item_price=item_price,
                    order=order,

                )
                # generate the recipt of order and save to db
                # AddtoEnrolled Course model
                user_enroll_course = user_model.EnrolledCourses.objects.create(
                    course=order_items.course,
                    student=order.student
                )
                # Delete Order Items from the Cart model
                delete_from_cart = models.Cart.objects.filter(
                    course=order_items.course,
                    student=order.student
                ).delete()
            # generate receipt in pdf
            order_items = models.OrderItems.objects.filter(
                order__id=order.id)
            data = {'order': order, 'order_items': order_items}
            pdf_receipt = receipt_render_to_pdf(
                'lms_main/receipt/receipt.html', data)
            # saving receipt to order model
            order.pdf_receipt = pdf_receipt
            order.save()
        except Exception as e:
            print("Error on payment success view:", e)
        else:

            print("success payment")
            context['order'] = order
            context['order_items'] = order_items

    return render(request, 'lms_main/payment/payment_success.html', context)


@login_required
def payment_failure_view(request):

    context = {

    }

    return render(request, 'lms_main/payment/payment_failure.html', context)
