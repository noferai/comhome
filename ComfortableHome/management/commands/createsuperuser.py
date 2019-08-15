from django.contrib.auth.management.commands import createsuperuser
from users.models import Admin


class Command(createsuperuser.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = Admin
        self.username_field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)
