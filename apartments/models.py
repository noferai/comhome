from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from users.models import Admin
from addresses.models import Address
from ComfortableHome.utils import ApartmentStatusChoices, ApartmentTypeChoices
from django.urls import reverse


class Apartment(models.Model):
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL, verbose_name="Адрес")
    apartment_number = models.PositiveSmallIntegerField('№ помещения')
    entrance = models.PositiveSmallIntegerField('Подъезд')
    floor = models.PositiveSmallIntegerField('Этаж')
    number_of_rooms = models.PositiveSmallIntegerField('Количество комнат')
    area = models.FloatField('Площадь', null=True, blank=True)
    number_of_business_account = models.PositiveIntegerField('№ лицевого счёта', unique=True)
    balance_of_business_account = models.IntegerField('Баланс лицевого счёта', default=0)
    created_by = models.ForeignKey(Admin, related_name='apartment_created_by', null=True, on_delete=models.SET_NULL)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)
    type = models.CharField('Тип помещения', choices=ApartmentTypeChoices.choices, max_length=64,
                            default=ApartmentTypeChoices.non_residential)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.address.__str__() + ", кв. " + str(self.apartment_number)

    def get_absolute_url(self):
        return reverse('apartments:view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'
        ordering = ['created_on']
