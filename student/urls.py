from django.urls import path
from . import views as student_views

app_name = 'student'


urlpatterns = [
    path('dashboard/', student_views.dashboard, name='dashboard'),
    path('my-course/', student_views.my_course, name='my-course'),
    path('my-course-detail/<slug:slug>',
         student_views.my_course_detail_view, name='my-course-detail'),
    path('my-course/track-video', student_views.track_video, name='track-video'),
    path('update_profile/', student_views.update_student_profile, name='update-profile'),


]
