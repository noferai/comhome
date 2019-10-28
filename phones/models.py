from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from clients.models import Client


class PhoneNumber(models.Model):
    number = PhoneNumberField('Телефон', unique=True)
    note = models.CharField('Заметка', blank=True, max_length=200)
    client = models.ForeignKey(Client, related_name='phones', on_delete=models.CASCADE)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)

    def __str__(self):
        if self.note:
            return str(self.number) + " (" + self.note + ")"
        else:
            return str(self.number)

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
        ordering = ['created_on']