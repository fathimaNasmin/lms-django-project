from django.shortcuts import render

def signup(request):
    return render(request,'user/signup.html')