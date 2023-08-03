from django.shortcuts import render,redirect

from . import forms

def signup(request):
    signup_form = forms.SignUpForm(request.POST or None)
    if signup_form.is_valid():
        signup_form.save()
        print(signup_form.cleaned_data['email'])
        return redirect('signup')
    context = {'form':signup_form}
    return render(request,'user/signup.html',context)