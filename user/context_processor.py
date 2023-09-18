from lms_main.models import Course
from student.models import Cart
from instructor.models import Category
from django.contrib.auth.decorators import login_required

def common_context(request):
    context = {}
    categories = Category.objects.all()
    courses = Course.objects.filter(status='PUBLISH').all()
    context['categories'] = categories
    context['courses'] = courses
    return context


def student_cart_count(request):
    if request.path.startswith('/admin/'):
        return {}
    if request.path.startswith('/instructor/'):
        return {}
    if request.user.is_authenticated:
        no_of_items_cart = Cart.objects.filter(student=request.user.student).count()
        return {'count' : no_of_items_cart }

    return {}
