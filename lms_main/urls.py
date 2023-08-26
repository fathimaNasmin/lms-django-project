from django.urls import path, include
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
    path('single-course/<slug:slug>/add-to-cart/',
         lms_main_view.add_to_cart, name='add-to-cart'),
    path('shopping-cart/',
         lms_main_view.shopping_cart, name='shopping-cart'),
    path('checkout/',
         lms_main_view.checkout, name='checkout'),
    path('save-for-later/',
         lms_main_view.save_for_later, name='save-for-later'),
    path('save-for-later-to-cart/',
         lms_main_view.save_for_later_to_cart, name='save-for-later-to-cart'),
    path('remove-from-cart/',
         lms_main_view.remove_from_cart, name='remove-from-cart'),
    # paypal urls
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment-success/',
         lms_main_view.payment_success_view, name='payment-success'),
    path('payment-failure/',
         lms_main_view.payment_failure_view, name='payment-failure'),

]
