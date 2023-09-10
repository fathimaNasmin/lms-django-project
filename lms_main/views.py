from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.db.models import Sum
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import json
import math
import random

# import:Models
from . import models
from user import models as user_model

from lms_main.templatetags import course_tags
from .utils import receipt_render_to_pdf, generate_order_number

#import forms
from user import forms as user_forms
from . import forms as lms_main_forms


def home_page(request):

    return render(request, 'lms_main/home.html')


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
    no_of_students_enrolled = user_model.EnrolledCourses.objects.filter(
        course__slug=slug).all().count()

    total_time_duration_course = sum([video.time_duration for video in videos])
    context = {}
    user = request.user
    # print(user.is_authenticated)

    # for video in videos:
    #     print("video id", video.lesson.id)
    context = {
        'course': single_course,
        'videos': videos,
        'total_time_duration_course': total_time_duration_course,
        'no_of_videos': videos.count(),
        'no_of_students_enrolled': no_of_students_enrolled,
    }
    if user.is_authenticated:
        user_enrolled_course = user_model.EnrolledCourses.objects.filter(
            course=single_course, student=user.student).exists()
        course_exists_in_cart = models.Cart.objects.filter(
            course=single_course, student=user.student)
        # print("user_enrolled_course:", user_enrolled_course)
        # print("course_exists_in_cart:", course_exists_in_cart)
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
        current_user_items_dict['id'] = item.course.id
        current_user_items_dict['title'] = item.course.title
        current_user_items_dict['slug'] = item.course.slug
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
                order_no=generate_order_number())
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
            redirect('lms_main:payment-failure')
        else:

            print("success payment")
            context['order'] = order
            context['order_items'] = order_items
            print(context)
    return render(request, 'lms_main/payment/payment_success.html', context)


@login_required
def payment_failure_view(request):

    context = {

    }

    return render(request, 'lms_main/payment/payment_failure.html', context)


# @login_required
# def order_receipt_view(request, order_no):
#     print(order_no)
#     pdf_doc = models.Order.objects.filter(
#         student=request.user.student, order_no=order_no)
#     print(pdf_doc)
#     response = HttpResponse(pdf_doc.pdf_receipt,
#                             content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename=f"receipt.pdf"'
#     return response
# =========INSTRUCTOR MODULE=================================
# ========================================INSTRUCTOR MODULE==============================================

# Signup view for instructors to create a new account
def instructor_signup(request):
    """View for creating a new account for the Instructor"""

    if request.method == 'POST' and request.is_ajax():
        signup_form = user_forms.SignUpForm(request.POST)
        data = {}
        if signup_form.is_valid():
            """form validation checking"""

            data['success'] = True
            new_instructor = signup_form.save()
            user = user_model.Instructor(instructor_id=new_instructor.id)
            user.save()
            # messages.success(request, 'Account created successfully')
            data['new_instructor_id'] = new_instructor.id
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data['success'] = False
            data['errors'] = signup_form.errors
            data['new_instructor_id'] = None
            # print("Validation Error")
            # print(signup_form.errors.as_json())
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        signup_form = user_forms.SignUpForm()

    context = {'form': signup_form}
    return render(request, 'user/instructor/instructor_signup.html', context)


def instructor_login(request):
    """View for authenticating Instructor"""

    if request.method == "POST" and request.is_ajax():
        form = user_forms.InstructorLoginForm(request, data=request.POST)
        data = {}
        if form.is_valid():
            email = form.cleaned_data['username']
            user = user_model.User.objects.get(email=email)

            if user is not None:
                login(request, user, backend='user.custom_auth_backend.EmailBackend')
                print(user.is_authenticated)
                print(request.user)
                instructor = user_model.Instructor.objects.filter(instructor=request.user.instructor).first()
                # print(instructor.values_list('instructor'))
                # Create a session to store instructor details
                request.session['logged_instructor'] = {
                    'email':instructor.instructor.email,
                    'full_name':instructor.instructor.full_name,
                    'profile_image':instructor.profile_image_url,
                    'about':instructor.about_me,
                    'designation': instructor.designation,
                    
                }
                print(request.session['logged_instructor'])
                data = {
                    'success': True,
                }
                return HttpResponse(json.dumps(data), content_type='application/json')

            else:
                data1['success'] = False
                data1['form'] = form.errors
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data1['form_errors'] = form.errors
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        form = user_forms.InstructorLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'user/instructor/instructor_login.html', context)



@login_required
def instructor_logout(request):
    logout(request)
    return redirect('lms_main:home')

@login_required
def instructor_dashboard(request):
    print("you are in dashboard")
    print(request.session['logged_instructor'])
    user = request.user
    data = {}
    
    
    # Instantiate forms
    add_course_form = lms_main_forms.AddCourseForm()
     # Inline Form set for requirement & what you will learn
    requirement_formset = lms_main_forms.RequirementFormSet()
    what_you_will_learn_formset = lms_main_forms.WhatYouWillLearnFormSet()
    
    
    instructor = user_model.Instructor.objects.filter(instructor_id=user.id).first()
    # print(instructor.course_set.all())
    
    # Posting the form       
    if request.method == "POST" and request.is_ajax():
        form_type = request.POST.get('form_type')
        print(form_type)
        print('lesson-submit-btn' in request.POST)
        
        # Course POST request
        if form_type == 'course-submit-btn':
            add_course_form = lms_main_forms.AddCourseForm(
                request.POST, request.FILES)
            requirement_formset = lms_main_forms.RequirementFormSet(request.POST)
            what_you_will_learn_formset = lms_main_forms.WhatYouWillLearnFormSet(
            request.POST)
            # print(request.POST)
            
            if add_course_form.is_valid() and requirement_formset.is_valid() and what_you_will_learn_formset.is_valid():
                # form validating & saving the form data to db
                data['success'] = True

                course_instance = add_course_form.save(commit=False)
                course_price = add_course_form.cleaned_data['price']
                if not course_price:
                    course_instance.price = 0
                course_instance.author = user.instructor
                course_instance.save()

                requirment_instance = requirement_formset.save(commit=False)
                for instance in requirment_instance:
                    instance.course = course_instance
                    instance.save()

                what_you_will_learn_instance = what_you_will_learn_formset.save(
                    commit=False)
                for instance in what_you_will_learn_instance:
                    instance.course = course_instance
                    instance.save()

                print("successfully saved")

                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                print(add_course_form.errors)
                print(requirement_formset.errors)
                data['course_form_errors'] = add_course_form.errors
                data['requirement_form_errors'] = requirement_formset.errors

                data['success'] = False
                return HttpResponse(json.dumps(data), content_type='application/json')
            
       
            
    context = {
        'instructor': instructor,
        'course_form': add_course_form,
        'requirement_formset': requirement_formset,
        'what_you_will_learn_formset': what_you_will_learn_formset,
    }
    return render(request, 'user/instructor/instructor_dashboard.html', context)
    

@login_required
def instructor_my_course(request, slug):
    """views to display the course details in instructor panel"""
    instructor = request.session.get('logged_instructor')
    data = {}
    # print(instructor)
    
    course_detail = models.Course.objects.filter(slug=slug).first()
    course_videos = course_detail.video_set.all()
    
    #  Lesson Form
    add_lesson_form = lms_main_forms.AddLessonForm()
    # Inline Form set for video
    video_formset = lms_main_forms.VideoFormSet()
    
    # Question Form
    question_form = lms_main_forms.QuestionForm()
    # Inline Form set for Options
    quiz_option_formset = lms_main_forms.QuizOptionFormSet()
    
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        if 'edit-link' in request.POST:
            lesson_id = request.POST.get("lesson_id")
            print(lesson_id)
            # lesson and video instance to initial in formset
            lesson_query = models.Lesson.objects.filter(id=lesson_id).defer('id','course_id')
            lesson_instance = [{'name':instance.name, 'course_id': instance.course_id} for instance in lesson_query]
            print(lesson_instance)
            
            # video_instance = models.Video.objects.filter(lesson__id=lesson_id).values()
            # Exclude the fields that are not required form queryset
            
            # Add initial to the formset
            add_lesson_form = lms_main_forms.AddLessonForm(request.POST, initial=lesson_instance)
            # video_formset = lms_main_forms.VideoFormSet(
            #     request.POST, initial=video_instance)
            # print(lesson_instance.id)
            # print(video_instance)
            data['success'] = True
            print(data)
            return HttpResponse(json.dumps(data), content_type='application/json')
    
        # lesson POST request
        if 'lesson-submit-btn' in request.POST:
            add_lesson_form = lms_main_forms.AddLessonForm(
                request.POST)
            video_formset = lms_main_forms.VideoFormSet(request.POST)
            print(request.POST)

            if add_lesson_form.is_valid() and video_formset.is_valid():
                data['success'] = True
                course = models.Course.objects.get(
                    id=request.POST['course_id'])
                print(course)
                # save Lesson to Model
                lesson_instance = add_lesson_form.save(commit=False)
                lesson_instance.course = course
                lesson_instance.save()

                # save videos to the Model
                video_instance = video_formset.save(
                    commit=False)
                for instance in video_instance:
                    instance.course = course
                    instance.lesson = lesson_instance
                    instance.save()

                return HttpResponse(json.dumps(data), content_type='application/json')

            else:
                data['success'] = False
                print(add_lesson_form.errors)
                print(video_formset.errors)
                data['lesson_form_errors'] = add_lesson_form.errors
                data['video_form_errors'] = video_formset.errors

                return HttpResponse(json.dumps(data), content_type='application/json')
    
        # Quiz POST request
        if 'quiz-form-btn' in request.POST:
            question_form = lms_main_forms.QuestionForm(request.POST)
            quiz_option_formset = lms_main_forms.QuizOptionFormSet(request.POST)
            
            if question_form.is_valid() and quiz_option_formset.is_valid():
                data['success'] = True
                try:
                    # store question_form to Question model
                    question_instance = question_form.save(commit=False)
                    question_instance.course = course_detail
                    question_instance.save()
                    print(question_form.cleaned_data)
                  
                    # store quiz_option_formset to the QuizOption model
                    option_instance = quiz_option_formset.save(commit=False)
                    for instance in option_instance:
                        instance.question_id = question_instance
                        instance.save()
                except Exception as e:
                    print(e)
                    print("error on saving...")
            
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data['success'] = False
                print("form validation failed")
                print(question_form.errors)
                print(quiz_option_formset.errors)

                return HttpResponse(json.dumps(data), content_type='application/json')
                
        
            
        
    context = {
        'instructor':instructor,
        'course': course_detail,
        'videos': course_videos,
        'lesson_form': add_lesson_form,
        'video_formset': video_formset,
        'question_form': question_form,
        'quiz_option_formset': quiz_option_formset,
        
    }
    return render(request, 'user/instructor/instructor_my_course.html', context)


@login_required
def instructor_delete_course(request):
    data = {}
    if request.method == "POST" and request.is_ajax():
        course_id = request.POST.get('course_id')
        print(course_id)
        try:
            query_course = models.Course.objects.get(id=course_id)
            print(query_course)
            query_course.delete()
            data['success'] = True
        except Exception as e:
            print("Exception",e)
            data['success'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def update_instructor_profile(request):
    """views function to update the user profile"""
    user = request.user
    if user:
        update_user_info = user_forms.SignUpForm(
            request.POST or None, instance=user)
        update_instructor = user_forms.InstructorUpdateForm(
            request.POST or None, request.FILES or None, instance=user.instructor)

        # Disable the email field for the signup form
        update_user_info.fields['email'].widget.attrs['readonly'] = True

        data = {}

        if request.method == 'POST' and request.is_ajax():
            if update_user_info.is_valid() and update_instructor.is_valid():
                obj = update_user_info.save(commit=False)
                obj1 = update_instructor.save(commit=False)

                obj.first_name = request.POST['first_name']
                obj.last_name = request.POST['last_name']

                update_user_info.save()
                update_instructor.save()

                login(request, user, backend='user.custom_auth_backend.EmailBackend')

                updated_data = {
                    'user_firstname': user.first_name,
                    'user_email': user.email,

                }
                data['success'] = True
                data['new_data'] = updated_data
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:

                data['success'] = False
                data['u_form_errors'] = update_user_info.errors
                data['i_form_errors'] = update_instructor.errors
                print(data['u_form_errors'])
                print(data['i_form_errors'])

                return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return redirect('lms_main:home')
    context = {
        'user': user,
        'u_form': update_user_info,
        'i_form': update_instructor
    }
    return render(request, 'user/instructor/instructor_update_profile.html', context)


@login_required
def instructor_edit_course(request, course_id):
    """views function to add new course by the instructor"""
    data = {}
    
    
    if request.method == "POST" and request.is_ajax():
        
        # Course POST request
        if 'course-submit-btn' in request.POST:
            print(request.POST)
        # lesson POST request   
        elif 'lesson-submit-btn' in request.POST:
            print(request.POST)
            
            
        
        
        

    context = {
        
    }

    return render(request, 'user/instructor/instructor_dashboard.html', context)
