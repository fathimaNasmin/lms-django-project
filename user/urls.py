from django.urls import path
from . import views as user_view

app_name = 'user'


urlpatterns = [
    path('signup/', user_view.signup, name='signup'),
    path('login/', user_view.login_user, name='login-user'),
    path('dashboard/', user_view.dashboard, name='dashboard'),
    path('logout/', user_view.logout_user, name='logout-user'),
]