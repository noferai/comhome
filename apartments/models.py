from django.db import models
from common.models import User
from catalog.models import Address
from requests.models import Request
from common.utils import ApartmentStatusChoices
from django.utils import timezone


class Apartment(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    apartment_number = models.PositiveSmallIntegerField('Номер квартиры')
    entrance = models.PositiveSmallIntegerField('Подъезд')
    floor = models.PositiveSmallIntegerField('Этаж')
    number_of_rooms = models.PositiveSmallIntegerField('Количество комнат')
    area = models.FloatField('Площадь', null=True, blank=True)
    number_of_business_account = models.IntegerField('Номер лицевого счёта', default=0)
    balance_of_business_account = models.IntegerField('Баланс лицевого счёта', default=0)
    created_by = models.ForeignKey(User, related_name='apartment_created_by', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField('Статус', choices=ApartmentStatusChoices.choices, max_length=64, default=ApartmentStatusChoices.empty)
    # request_history = models.ForeignKey(Case, on_delete=models.PROTECT)
