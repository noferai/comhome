from django.db import models

from common.models import User
from common.utils import StaffOccupationChoices
from phonenumber_field.modelfields import PhoneNumberField


class Staff(models.Model):
    name = models.CharField('ФИО', max_length=64)
    email = models.EmailField('Email', blank=True)
    phone = PhoneNumberField('Телефон', null=True)
    industry = models.CharField('Тип деятельности', max_length=255, choices=StaffOccupationChoices.choices, blank=True, null=True)
    description = models.TextField('Комментарий', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='account_created_by', on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField('Добавлен', auto_now_add=True)
    is_active = models.BooleanField('Свободен', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
