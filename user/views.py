from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


from . import forms as user_forms
from lms_main import forms as lms_main_forms

import json
# importing models
from .models import Student,User

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
def logout_user(request):
    logout(request)
    return redirect('lms_main:home')


