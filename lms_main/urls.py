from django.urls import path
from . import views as lms_main_view


app_name = 'lms_main'


urlpatterns = [
    path('', lms_main_view.home_page, name='home'),
    path('categoty-detail/<int:id>/', lms_main_view.category_detail, name='category-detail'),
    path('course-lists/', lms_main_view.course_lists, name='course-lists'),
    path('single-course/<int:id>/', lms_main_view.single_course, name='single-course'),
    
]