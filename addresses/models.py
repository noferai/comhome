from django.db import models
from ComfortableHome.utils import CityChoices


class Address(models.Model):
    city = models.CharField('Город', choices=CityChoices.choices, max_length=100)
    street = models.CharField('Улица', max_length=500)
    building = models.CharField('Здание', max_length=50)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)

    def __str__(self):
        return ', '.join(['г. ' + self.city, self.street, self.building])

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['created_on']
