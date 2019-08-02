from django.db import models
from django.utils import timezone


class Address(models.Model):
    address_str = models.CharField('Адрес', max_length=500)
    created_date = models.DateField('Дата', default=timezone.now)

    def __str__(self):
        return self.address_str

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Services(models.Model):
    name_of_service = models.CharField('Группа услуг', max_length=1000)
    debt_at_beg_of_period = models.FloatField('Задолженность на начало периода')
    accrued = models.FloatField('Начислено')
    recalculations = models.FloatField('Перерасчёты')
    paid = models.FloatField('Оплачено')
    debt_at_end_of_period = models.FloatField('Задолженность на конец периода')
    created_date = models.DateField('Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Document(models.Model):
    # type_of_document
    # name
    # author
    # file
    pass
