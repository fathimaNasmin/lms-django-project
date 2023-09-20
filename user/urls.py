from django.urls import path
from . import views as user_view
from lms_main import views as lms_main_views

app_name = 'user'


urlpatterns = [
    path('signup/', user_view.signup, name='signup'),
    path('login/', user_view.login_user, name='login-user'),

    path('logout/', user_view.logout_user, name='logout-user'),
    

    
]
