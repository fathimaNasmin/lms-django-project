from django.urls import path
from . import views as lms_main_view


app_name = 'lms_main'


urlpatterns = [
    path('', lms_main_view.home_page, name='home'),
    path('search/', lms_main_view.search, name='search'),
    path('category-detail/<slug:slug>/',
         lms_main_view.category_detail, name='category-detail'),
    path('course-lists/', lms_main_view.course_lists, name='course-lists'),
    path('single-course/<slug:slug>/',
         lms_main_view.single_course, name='single-course'),
    path('single-course/<slug:slug>/enroll-course/',
         lms_main_view.enroll_course, name='enroll-course'),

]
