from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

import json
import math
import random

# import:Models
from . import models as instructor_models
from user import models as user_model
from student import models as student_model

from lms_main.templatetags import course_tags
from lms_main.utils import receipt_render_to_pdf, generate_order_number

# import forms
from user import forms as user_forms
from lms_main import forms as lms_main_forms


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
    return render(request, 'instructor/instructor_signup.html', context)


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
                instructor = user_model.Instructor.objects.filter(
                    instructor=request.user.instructor).first()
                # print(instructor.values_list('instructor'))
                # Create a session to store instructor details
                request.session['logged_instructor'] = {
                    'email': instructor.instructor.email,
                    'full_name': instructor.instructor.full_name,
                    'profile_image': instructor.profile_image_url,
                    'about': instructor.about_me,
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
    return render(request, 'instructor/instructor_login.html', context)


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

    instructor = user_model.Instructor.objects.filter(
        instructor_id=user.id).first()
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
            requirement_formset = lms_main_forms.RequirementFormSet(
                request.POST)
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
    return render(request, 'instructor/instructor_dashboard.html', context)


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
            lesson_query = instructor_models.Lesson.objects.filter(
                id=lesson_id).defer('id', 'course_id')
            lesson_instance = [
                {'name': instance.name, 'course_id': instance.course_id} for instance in lesson_query]
            print(lesson_instance)

            # video_instance = models.Video.objects.filter(lesson__id=lesson_id).values()
            # Exclude the fields that are not required form queryset

            # Add initial to the formset
            add_lesson_form = lms_main_forms.AddLessonForm(
                request.POST, initial=lesson_instance)
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
            quiz_option_formset = lms_main_forms.QuizOptionFormSet(
                request.POST)

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
        'instructor': instructor,
        'course': course_detail,
        'videos': course_videos,
        'lesson_form': add_lesson_form,
        'video_formset': video_formset,
        'question_form': question_form,
        'quiz_option_formset': quiz_option_formset,

    }
    return render(request, 'instructor/instructor_my_course.html', context)


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
            print("Exception", e)
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
    return render(request, 'instructor/instructor_update_profile.html', context)


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

    return render(request, 'instructor/instructor_dashboard.html', context)
