from django.urls import path
from . import views as lms_main_view


app_name = 'lms_main'


urlpatterns = [
    path('', lms_main_view.home_page, name='home'),
]