from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from staff.models import Staff
from users.models import User
from apartments.models import Apartment
from homeowners.utils import RequestChoicesGender, RequestChoicesDebtStatus, \
    RequestChoicesGarbagePayment, RequestChoicesTypePassport


class Homeowner(User):
    gender = models.CharField('Пол', max_length=10, choices=RequestChoicesGender.choices, null=True)
    birthday = models.DateField('Дата рождения', null=True)
    debt = models.BooleanField('Задолженность', null=True)
    status_of_work_with_debt = models.CharField('Статус работы по взысканию задолженности',
                                                max_length=255, choices=RequestChoicesDebtStatus.choices,
                                                blank=True, null=True)
    garbage_payment = models.BooleanField('Задолженность по мусору', null=True,
                                          choices=RequestChoicesGarbagePayment.choices)
    date_of_issue = models.DateField('Дата выдачи паспорта', null=True)
    apartments = models.ManyToManyField(Apartment, related_name='homeowner', blank=True)
    comments = GenericRelation(Comment)

    # Поля паспорта
    passport_date = models.DateField('Дата выдачи', null=True)
    passport_series = models.IntegerField('Серия паспорта', null=True)
    passport_id = models.IntegerField('Номер паспорта', null=True)
    issued_by = models.CharField('Кем выдан', max_length=100, null=True)
    unit_code = models.IntegerField('Код подразделения', null=True)
    type_of_passport = models.CharField('Тип паспорта', max_length=100, null=True,
                                        choices=RequestChoicesTypePassport.choices)

    # Поля информации
    birthday_reminder = models.BooleanField('Напоминание о Дне Рождения')
    hard_case = models.BooleanField('Проблемный')
    loyal = models.BooleanField('Лояльный')
    vip = models.BooleanField('VIP')
    calls = models.BooleanField('Звонки')
    sms = models.BooleanField('СМС')
    mail = models.BooleanField('Email')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('homeowners:view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Собственник'
        verbose_name_plural = 'Собственники'
        ordering = ['-date_joined']
