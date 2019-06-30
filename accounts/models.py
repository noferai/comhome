from django.db import models

from common.models import User, Address, Team
from common.utils import StaffOccupationChoices
from phonenumber_field.modelfields import PhoneNumberField


class Account(models.Model):
    name = models.CharField('ФИО', max_length=64)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField('Телефон', null=True)
    industry = models.CharField('Тип деятельности', max_length=255, choices=StaffOccupationChoices.choices, blank=True, null=True)
    description = models.TextField('Комментарий', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='account_created_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField('Добавлен', auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']
