from django.db import models
from apartments.models import Apartment


class Invoice(models.Model):
    name = models.CharField('Группа услуг', max_length=1000)
    accrued = models.FloatField('Начислено')
    paid = models.FloatField('Оплачено')
    apartment = models.OneToOneField(Apartment, on_delete=models.DO_NOTHING)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)

    class Meta:
        verbose_name = 'Взаиморасчет'
        verbose_name_plural = 'Взаиморасчеты'
        ordering = ['-created_on']