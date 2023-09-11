from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


from . import forms as user_forms
from lms_main import forms as lms_main_forms
import json
from django.contrib import messages
from .models import Student, Instructor, User, EnrolledCourses
from lms_main.models import Course, Video
from .custom_auth_backend import EmailBackend

from lms_app import settings


def signup(request):
    """View for creating a new account for the student"""

    if request.method == 'POST' and request.is_ajax():
        signup_form = user_forms.SignUpForm(request.POST)
        data = {}
        if signup_form.is_valid():
            """form validation checking"""

            data['success'] = True
            new_user = signup_form.save()
            user = Student(student_id=new_user.id)
            user.save()
            # messages.success(request, 'Account created successfully')
            data['new_user_id'] = new_user.id
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data['success'] = False
            data['errors'] = signup_form.errors
            data['new_user_id'] = None
            # print("Validation Error")
            # print(signup_form.errors.as_json())
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        signup_form = user_forms.SignUpForm()

    context = {'form': signup_form}
    return render(request, 'user/signup.html', context)


def login_user(request):
    """View for authenticating student"""

    if request.method == "POST" and request.is_ajax():
        form = user_forms.LoginForm(request, data=request.POST)
        data1 = {}
        if form.is_valid():
            email = form.cleaned_data['username']
            user = User.objects.get(email=email)

            if user is not None:
                login(request, user, backend='user.custom_auth_backend.EmailBackend')
                print(user.is_authenticated)

                if 'next' in request.POST:
                    next_url = request.POST.get('next')
                    data1 = {
                        'success': True,
                        'next': next_url,
                    }
                    return HttpResponse(json.dumps(data1), content_type='application/json')
                else:
                    data1 = {
                        'success': True,
                    }
                    return HttpResponse(json.dumps(data1), content_type='application/json')

            else:
                data1['success'] = False
                data1['form'] = form.errors
                return HttpResponse(json.dumps(data1), content_type='application/json')
        else:
            data1['form_errors'] = form.errors
            return HttpResponse(json.dumps(data1), content_type='application/json')
    else:
        form = user_forms.LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'user/login.html', context)


@login_required
def dashboard(request):
    print("you are in dashboard")
    user = request.user
    my_courses = EnrolledCourses.objects.filter(student=user.student)
    
    if user:
        context = {
            'user': user,
            'my_courses': my_courses,
        }
        return render(request, 'user/dashboard.html', context)
    return Http404

# View:lists all the enrolled courses by the logged in student


@login_required
def my_course(request):
    user = request.user
    my_courses = EnrolledCourses.objects.filter(student=user.student)

    context = {
        'my_courses': my_courses,
    }
    print(context)

    for course in my_courses:
        print(course)
    return render(request, 'user/my_course.html', context)



# View for detailed course for enrolled course
@login_required
def my_course_detail_view(request, slug):
    course_video = Video.objects.filter(course__slug=slug)
    print(course_video)
    context = {
        'videos': course_video,
    }
    return render(request,'user/my_course_detail.html', context)



@login_required
def update_student_profile(request):
    """views function to update the user profile"""
    user = request.user
    if user:
        update_user_info = user_forms.SignUpForm(
            request.POST or None, instance=user)
        update_profile_image = user_forms.UpdateProfileForm(
            request.POST or None, request.FILES or None, instance=user.student)

        # Disable the email field for the signup form
        update_user_info.fields['email'].widget.attrs['readonly'] = True

        data = {}

        if request.method == 'POST' and request.is_ajax():
            if update_user_info.is_valid() and update_profile_image.is_valid():
                obj = update_user_info.save(commit=False)
                obj1 = update_profile_image.save(commit=False)

                obj.first_name = request.POST['first_name']
                obj.last_name = request.POST['last_name']

                update_user_info.save()
                update_profile_image.save()

                login(request, request.user,
                      backend='user.custom_auth_backend.EmailBackend')

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
                data['p_form_errors'] = update_profile_image.errors
                print(data['u_form_errors'])
                print(data['p_form_errors'])

                return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return redirect('lms_main:home')
    context = {
        'user': user,
        'u_form': update_user_info,
        'p_form': update_profile_image
    }
    return render(request, 'user/user_profile.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('lms_main:home')


