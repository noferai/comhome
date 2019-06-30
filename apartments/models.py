from django.db import models
from common.models import User
from catalog.models import Address
from cases.models import Case
from common.utils import ApartmentStatusChoices


class Apartment(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    entrance = models.PositiveSmallIntegerField('Подъезд')
    floor = models.PositiveSmallIntegerField('Этаж')
    number_of_rooms = models.PositiveSmallIntegerField('Количество комнат')
    area = models.FloatField('Площадь', null=True, blank=True)
    business_account = models.CharField('Лицевой счет', max_length=500)
    created_by = models.ForeignKey(User, related_name='apartment_created_by', on_delete=models.CASCADE)
    status = models.CharField('Статус', choices=ApartmentStatusChoices.choices, max_length=64, default=ApartmentStatusChoices.empty)
    #request_history = models.ForeignKey(Case, on_delete=models.PROTECT)
    #owners = models.ManyToManyField()