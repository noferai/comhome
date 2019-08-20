from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from homeowners.models import Homeowner


class PhoneNumber(models.Model):
    number = PhoneNumberField('Телефон')
    note = models.CharField('Заметка', blank=True, max_length=200)
    homeowner = models.ForeignKey(Homeowner, related_name='phones', on_delete=models.CASCADE)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)

    def __str__(self):
        return str(self.number) + " (" + self.note + ")"

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
        ordering = ['created_on']