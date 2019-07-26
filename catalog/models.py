from django.db import models


class Address(models.Model):
    address = models.CharField('Адрес', max_length=500)

    def __str__(self):
        return self.address


class Services(models.Model):
    name_of_service = models.CharField('Группа услуг', max_length=1000)
    debt_at_beg_of_period = models.FloatField('Задолженность на начало периода')
    accrued = models.FloatField('Начислено')
    recalculations = models.FloatField('Перерасчёты')
    paid = models.FloatField('Оплачено')
    debt_at_end_of_period = models.FloatField('Задолженность на конец периода')


class Document(models.Model):
    # type_of_document
    # name
    # author
    # file
    pass
