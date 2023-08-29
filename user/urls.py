from django.urls import path
from . import views as user_view
from lms_main import views as lms_main_views

app_name = 'user'


urlpatterns = [
    path('signup/', user_view.signup, name='signup'),
    path('login/', user_view.login_user, name='login-user'),
    path('dashboard/', user_view.dashboard, name='dashboard'),
    path('my-course/', user_view.my_course, name='my-course'),

    path('logout/', user_view.logout_user, name='logout-user'),
    path('update_profile/', user_view.update_student_profile, name='update-profile'),

    
]
