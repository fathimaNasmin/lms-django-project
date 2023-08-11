from django.shortcuts import render
from django.http import HttpResponse



def home_page(request):
    if request.session.has_key('user_profile'):
        current_user = request.session.get('user_profile')
        print(current_user)
        return render(request, 'lms_main/home.html',{'user': current_user})

    return render(request, 'lms_main/home.html')
