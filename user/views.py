from django.shortcuts import render,redirect
from django.http import HttpResponse

from . import forms
import json
from django.contrib import messages

def signup(request):
    """View for creating a new account for the student"""

    if request.method == 'POST' and request.is_ajax():
        signup_form = forms.SignUpForm(request.POST)
        data = {}
        if signup_form.is_valid():
            data['success'] = True
            new_user = signup_form.save()

            student = forms.Student.objects.create(user=new_user, **profile_data)

            messages.success(request, 'Account created successfully')
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data['success'] = False
            print("Validation Error")
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        signup_form = forms.SignUpForm()


    context = {'form':signup_form}
    return render(request,'user/signup.html',context)