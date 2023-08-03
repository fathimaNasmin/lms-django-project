from django.urls import path
from . import views as user_view

app_name = 'user'


urlpatterns = [
    path('signup/', user_view.signup, name='signup'),
]