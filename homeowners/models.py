from django.db import models

from staff.models import Staff
from common.models import User
from apartments.models import Apartment
from homeowners.utils import RequestChoicesGender, RequestChoicesDebtStatus,\
    RequestChoicesDebt, RequestChoicesGarbagePayment, RequestChoicesTypePassport


class Homeowner(models.Model):
    name = models.CharField('ФИО', max_length=255, null=True)
    gender = models.CharField('Пол', max_length=10, choices=RequestChoicesGender.choices, null=True)
    email = models.EmailField()
    phone = models.CharField('Телефон', max_length=255)
    birthday = models.DateField('Дата рождения', null=True)
    debt = models.BooleanField('Задолженность', null=True, choices=RequestChoicesDebt.choices)
    status_of_work_with_debt = models.CharField('Статус работы по взысканию задолженности',
                                                max_length=255, choices=RequestChoicesDebtStatus.choices,
                                                blank=True, null=True)
    garbage_payment = models.BooleanField('Задолженность по мусору', null=True,
                                          choices=RequestChoicesGarbagePayment.choices)
    date_of_issue = models.DateField('Дата выдачи паспорта', null=True)
    apartments = models.ManyToManyField(Apartment, related_name='owners', blank=True)

    # Поля паспорта
    passport_date = models.DateField('Дата выдачи', null=True)
    passport_series = models.IntegerField('Серия паспорта', null=True)
    passport_id = models.IntegerField('Номер паспорта', null=True)
    issued_by = models.CharField('Кем выдан', max_length=100, null=True)
    unit_code = models.IntegerField('Код подразделения', null=True)
    type_of_passport = models.CharField('Тип паспорта', max_length=100, null=True, choices=RequestChoicesTypePassport.choices)

    # Поля информации
    birthday_reminder = models.BooleanField('Напоминание о Дне Рождения', null=True, choices=RequestChoicesDebt.choices)
    hard_case = models.BooleanField('Проблемный', null=True, choices=RequestChoicesDebt.choices)
    loyal = models.BooleanField('Лояльный', null=True, choices=RequestChoicesDebt.choices)
    vip = models.BooleanField('VIP', null=True, choices=RequestChoicesDebt.choices)
    calls = models.BooleanField('Звонки', null=True, choices=RequestChoicesDebt.choices)
    sms = models.BooleanField('СМС', null=True, choices=RequestChoicesDebt.choices)
    mail = models.BooleanField('Email', null=True, choices=RequestChoicesDebt.choices)
    comments = models.TextField('Комментарий', blank=True)
    created_by = models.ForeignKey(User, related_name='lead_created_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name
