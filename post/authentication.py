from django.contrib.auth.forms import User


class EmailAuthbackend():
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist as e:
            return None

    def get_user(self, user_id):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            return None
