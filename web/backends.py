from django.contrib.auth.backends import ModelBackend
from .models.user_model import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email', username)
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            return None
        print(user.check_password(password))
        if user.check_password(password):
            return user
        return None
