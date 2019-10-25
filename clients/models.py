from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from users.models import Admin
from comment.models import Comment
from staff.models import Staff
from users.models import User
from apartments.models import Apartment
from ComfortableHome.utils import ClientGenderChoices, ClientTypeChoices


class Client(User):
    type = models.CharField('Тип клиента', max_length=10, choices=ClientTypeChoices.choices,
                            default=ClientTypeChoices.individual)
    gender = models.CharField('Пол', max_length=10, choices=ClientGenderChoices.choices,
                              default=ClientGenderChoices.none)
    birthday = models.DateField('Дата рождения', blank=True)
    apartments = models.ManyToManyField(Apartment, related_name='client')
    car_numbers = models.CharField("Номера автомобилей", max_length=2000, blank=True)
    registration = models.CharField("Место регистрации", max_length=2000)
    passport = models.CharField('Паспортные данные', max_length=5000, blank=True)
    comments = GenericRelation(Comment)

    # Поля информации
    calls = models.BooleanField('Звонки')
    sms = models.BooleanField('СМС')
    mail = models.BooleanField('Email')

    def get_absolute_url(self):
        return reverse('clients:view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-date_joined']
