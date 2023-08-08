from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from . import forms
import json
from django.contrib import messages
from .models import Student, Instructor, User

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
    form = forms.LoginForm(request.POST or None)
    if request.method == "POST" and request.is_ajax():
        data = {}
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            print(type(user))
            if user is not None:
                login(request, user)
                print("success")
                data = {
                    'success': True,
                }
                return HttpResponse(json.dumps(data), content_type='application/json')

            else:
                data['success'] = False
                data['form'] = form.errors
                return HttpResponse(json.dumps(data), content_type='application/json')

    context = {
        'form': form,
    }
    if form.errors:
        print(form.errors)
    return render(request,'user/login.html', context)

@login_required
def dashboard(request):
    print("you are in dashboard")
    return render(request,'user/dashboard.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('lms_main:home')
    
    