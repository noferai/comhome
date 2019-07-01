from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from accounts.models import Account
from common.models import User, Address, Team
from common.utils import LEAD_STATUS, LEAD_SOURCE
from leads.utils import RequestChoicesGender, RequestChoicesDebtStatus,\
    RequestChoicesDebt, RequestChoicesGarbagePayment, RequestChoicesTypePassport
from phonenumber_field.modelfields import PhoneNumberField


class Lead(models.Model):
    # Мои поля
    name = models.CharField('ФИО', max_length=255, null=True)
    gender = models.CharField('Пол', max_length=10, choices=RequestChoicesGender.choices, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField('Телефон', max_length=255)
    birthday = models.DateField('Дата рождения', blank=True, null=True)
    debt = models.BooleanField('Задолженность', null=True, choices=RequestChoicesDebt.choices)
    status_of_work_with_debt = models.CharField('Статус работы по взысканию задолженности',
                                                max_length=255, choices=RequestChoicesDebtStatus.choices,
                                                blank=True, null=True)
    garbage_payment = models.BooleanField('Задолженность по мусору', null=True,
                                          choices=RequestChoicesGarbagePayment.choices)
    date_of_issue = models.DateField('Дата выдачи паспорта', null=True)

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
    comments = models.TextField('Комментарий', null=True)


    # history_of_appeals = models.ForeignKey()
    # documents = models.ForeignKey
    # mutual_settlements = models.ForeignKey()

    # Тут ебал индусов и вообще всё ваше казино блять

    account = models.ForeignKey(Account, related_name='Leads', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(_("Status of Lead"), max_length=255,
                              blank=True, null=True, choices=LEAD_STATUS)
    source = models.CharField(_("Source of Lead"), max_length=255,
                              blank=True, null=True, choices=LEAD_SOURCE)
    address = models.ForeignKey(Address, related_name='leadaddress', on_delete=models.CASCADE, null=True, blank=True)
    website = models.CharField(_("Website"), max_length=255, blank=True, null=True)
    description = models.TextField('Примечания', blank=True, null=True)
    assigned_to = models.ManyToManyField(User, related_name='lead_assigned_users')
    teams = models.ManyToManyField(Team)
    account_name = models.CharField(max_length=255, null=True, blank=True)
    opportunity_amount = models.DecimalField(
        _("Opportunity Amount"), decimal_places=2, max_digits=12,
        blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='lead_created_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField('Добавлен', auto_now_add=True)
    is_active = models.BooleanField(default=False)
    enquery_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering =['-created_on']

    def __str__(self):
        return self.name
