from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import time


def img_url(filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, password):
        if not email:
            raise ValueError('Укажите email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user


class AdminManager(UserManager):
    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    file_prepend = "users/profile_pics"
    name = models.CharField('ФИО', max_length=150, blank=True)
    email = models.EmailField('Email', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField('Дата', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)
    profile_pic = models.FileField('Аватар', max_length=1000, upload_to=img_url, null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __unicode__(self):
        return self.email


class Admin(User):
    def get_absolute_url(self):
        return reverse('users:view', args=[str(self.id)])

    objects = AdminManager()

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
        ordering = ['-date_joined']
