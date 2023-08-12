from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm 


from . import forms
import json
from django.contrib import messages
from .models import Student, Instructor, User

from lms_app import settings

def signup(request):
    """View for creating a new account for the student"""

    if request.method == 'POST' and request.is_ajax():
        signup_form = forms.SignUpForm(request.POST)
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
        signup_form = forms.SignUpForm()


    context = {'form':signup_form}
    return render(request,'user/signup.html',context)



def login_user(request):
    """View for authenticating student"""
    
    if request.method == "POST" and request.is_ajax():
        form = forms.LoginForm(request, data=request.POST)
        data1 = {}
        if form.is_valid():
            email = form.cleaned_data['username']
            user = User.objects.get(email=email)
            
            if user is not None:
                login(request, user, backend='user.custom_auth_backend.EmailBackend')
                print(user.is_authenticated)
                # User profile from user obj is stored in the session
                user_profile = {
                    'user_id': user.id,
                    'user_firstname': user.first_name,
                    'user_last_name': user.last_name,
                    'user_email': user.email,
                    'user_is_student': True,
                    'student_id': user.student.student_id,
                    'user_is_authenticated': user.is_authenticated,
                    'profile_image': user.student.profile_image.url,
                    
                }
                request.session['user_profile'] = user_profile

                data1 = {
                    'success': True,
                    'student_name': user.first_name,
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
        form = forms.LoginForm()
    context = {
        'form': form,
    }
    return render(request,'user/login.html', context)

@login_required
def dashboard(request):
    print("you are in dashboard")
    if request.session.has_key('user_profile'):
        current_user = request.session.get('user_profile')
        print(current_user)
        context = {
        'user': current_user,
        }
        return render(request, 'user/dashboard.html', context)
    return redirect('lms_main:home')
    

@login_required
def update_student_profile(request):
    """views function to update the user profile"""
    #return 404 page
    
    if request.session.has_key('user_profile'):
        current_user = request.session.get('user_profile')
        logged_user_instance = User.objects.get(id=current_user['user_id'])
        logged_student_instance = Student.objects.get(student_id=logged_user_instance.id)


        update_user_info = forms.SignUpForm(request.POST or None, request.POST or None, instance=logged_user_instance)

        update_profile_image = forms.UpdateProfileForm(request.POST or None, request.FILES or None, instance=logged_student_instance)

        # Disable the email field for the signup form
        update_user_info.fields['email'].widget.attrs['readonly'] = True
        
        data = {}

        if request.method == 'POST' and request.is_ajax():
            if update_user_info.is_valid() and update_profile_image.is_valid():
                obj= update_user_info.save(commit= False)
                obj.first_name = update_user_info.cleaned_data.get('first_name')
                obj.last_name = update_user_info.cleaned_data.get('last_name')
                update_user_info.save()
                update_profile_image.save()

                data['success'] = True

                return HttpResponse(json.dumps(data), content_type='application/json')
            else:

                data['success'] = False
                data['u_form_errors'] = update_user_info.errors
                data['p_form_errors'] = update_profile_image.errors
                print(data['u_form_errors'])
                print(data['p_form_errors'])

                return HttpResponse(json.dumps(data), content_type='application/json')
        # else:
        #     data['failure'] = True
        #     return HttpResponse(json.dumps(data), content_type='application/json')
    

        context = {
        'user': current_user,
        'u_form': update_user_info,
        'p_form': update_profile_image
        }
        return render(request, 'user/user_profile.html', context)

    return '<h1>404 Not Foud</h1>'


@login_required
def logout_user(request):
    logout(request)
    return redirect('lms_main:home')

# ========================================INSTRUCTOR MODULE==============================================


def instructor_signup(request):
    """View for creating a new account for the Instructor"""

    if request.method == 'POST' and request.is_ajax():
        signup_form = forms.SignUpForm(request.POST)
        data = {}
        if signup_form.is_valid():
            """form validation checking"""

            data['success'] = True
            new_instructor = signup_form.save()
            user = Instructor(instructor_id=new_instructor.id)
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
        signup_form = forms.SignUpForm()


    context = {'form':signup_form}
    return render(request,'user/instructor/instructor_signup.html',context)



def instructor_login(request):
    """View for authenticating Instructor"""
    
    if request.method == "POST" and request.is_ajax():
        form = forms.InstructorLoginForm(request, data=request.POST)
        data = {}
        if form.is_valid():
            email = form.cleaned_data['username']
            user = User.objects.get(email=email)
            
            if user is not None:
                login(request, user, backend='user.custom_auth_backend.EmailBackend')
                print(user.is_authenticated)
                # User profile from user obj is stored in the session
                instructor_profile = {
                    'user_id': user.id,
                    'user_firstname': user.first_name,
                    'user_last_name': user.last_name,
                    'user_email': user.email,
                    'user_is_instructor': True,
                    'instructor_id': user.instructor.instructor_id,
                    'user_is_authenticated': user.is_authenticated,
                }
                request.session['instructor_profile'] = instructor_profile

                data = {
                    'success': True,
                    'instructor_name': user.first_name,
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
        form = forms.InstructorLoginForm()
    context = {
        'form': form,
    }
    return render(request,'user/instructor/instructor_login.html', context)

@login_required
def instructor_dashboard(request):
    print("you are in dashboard")
    if request.session.has_key('instructor_profile'):
        current_user = request.session.get('instructor_profile')
        print(current_user)
        context = {
        'user': current_user,
        }
        return render(request, 'user/instructor/instructor_dashboard.html', context)


@login_required
def update_instructor_profile(request):
    """views function to update the user profile"""
    if request.session.has_key('user_profile'):
        current_user = request.session.get('user_profile')
        print(current_user)
        context = {
        'user': current_user,
        }
        return render(request, 'user/instructor/instructor_update_profile.html', context)


@login_required
def instructor_logout(request):
    logout(request)
    return redirect('lms_main:home')




    
    