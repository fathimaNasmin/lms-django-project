from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model
from .models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        








