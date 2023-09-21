from django.urls import path, include
from . import views as instructor_view


app_name = 'instructor'  

urlpatterns = [
    path('instructor-signup/', instructor_view.instructor_signup,
         name='instructor-signup'),
    
    path('instructor-login/',
         instructor_view.instructor_login, name='instructor-login'),
    
    path('instructor-logout/', instructor_view.instructor_logout,
         name='instructor-logout'),
    path('instructor-dashboard/', instructor_view.instructor_dashboard,
         name='instructor-dashboard'),
    path('instructor-dashboard/my-course/<slug:slug>/', instructor_view.instructor_my_course,
         name='instructor-my-course'),
    path('instructor-dashboard/delete-course', instructor_view.instructor_delete_course,
         name='instructor-delete-course'),

    path('instructor-edit-course/', instructor_view.instructor_edit_course,
         name='instructor-edit-course'),

    path('instructor-update-profile/', instructor_view.update_instructor_profile,
         name='instructor-update-profile'),

]
