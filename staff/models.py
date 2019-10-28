from django.db import models
from django.urls import reverse
from users.models import User
from ComfortableHome.utils import StaffOccupationChoices
from phonenumber_field.modelfields import PhoneNumberField


class Staff(models.Model):
    name = models.CharField('ФИО', max_length=64)
    email = models.EmailField('Email', blank=True)
    phone = PhoneNumberField('Телефон', null=True)
    occupation = models.CharField('Тип деятельности', max_length=255, choices=StaffOccupationChoices.choices,
                                  default=StaffOccupationChoices.none)
    created_by = models.ForeignKey(User, related_name='account_created_by', on_delete=models.DO_NOTHING)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)
    is_active = models.BooleanField('Свободен', default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('staff:view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ['created_on']
