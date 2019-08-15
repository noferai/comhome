from django.contrib.auth.backends import ModelBackend
from users.models import User
from model_utils.managers import InheritanceQuerySet


class UserModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return InheritanceQuerySet(User).select_subclasses().get(pk=user_id)
        except User.DoesNotExist:
            return None
