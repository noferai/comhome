from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from staff.models import Staff
from users.models import User
from clients.models import Client
from apartments.models import Apartment
from ComfortableHome.utils import RequestTypeChoices, RequestPriorityChoices, RequestStatusChoices


class Request(models.Model):
    status = models.CharField('Статус', choices=RequestStatusChoices.choices, max_length=64,
                              default=RequestStatusChoices.new)
    priority = models.CharField('Приоритет', choices=RequestPriorityChoices.choices, max_length=64,
                                default=RequestPriorityChoices.medium)
    request_type = models.CharField('Тип заявки', choices=RequestTypeChoices.choices, max_length=255, blank=True,
                                    null=True, default=RequestTypeChoices.other)
    assigned_to = models.ManyToManyField(Staff, blank=True, related_name='request', verbose_name="Исполнители")
    closed_on = models.DateField('Закрыта', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='request_created_by', on_delete=models.DO_NOTHING)
    applicant = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Заявитель")
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name="Помещение")
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)
    is_proceed = models.BooleanField('В работе', default=False)

    def __str__(self):
        return self.priority + ': ' + self.request_type + ' - ' + self.applicant.name

    def get_assigned_staff(self):
        return Staff.objects.get(id=self.assigned_to.id)

    def get_absolute_url(self):
        return reverse('requests:view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['created_on']
