from django.db import models
from clients.models import Client
from apartments.models import Apartment
from ComfortableHome.utils import DocumentTypeChoices


class Document(models.Model):
    type = models.CharField("Тип документа", choices=DocumentTypeChoices.choices, max_length=200)
    date = models.DateField("Дата")
    note = models.TextField("Комментарий", blank=True)
    attachment = models.FileField("Прикрепления", upload_to='documents/%Y/%m/', blank=True)
    apartment = models.ForeignKey(Apartment, related_name='documents', null=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='documents', null=True, on_delete=models.CASCADE)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)

    def __str__(self):
        return self.type + " (" + str(self.date) + ")"

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['created_on']

