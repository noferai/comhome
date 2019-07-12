from django.db import models
from django.contrib.contenttypes.models import ContentType
from staff.models import Staff
from common.models import User
from common.utils import RequestTypeChoices, RequestPriorityChoices, RequestStatusChoices


class Request(models.Model):
    status = models.CharField('Статус', choices=RequestStatusChoices.choices, max_length=64, default=RequestStatusChoices.new)
    priority = models.CharField('Приоритет', choices=RequestPriorityChoices.choices, max_length=64, default=RequestPriorityChoices.normal)
    request_type = models.CharField('Тип поломки', choices=RequestTypeChoices.choices, max_length=255, blank=True, null=True, default=RequestTypeChoices.other)
    assigned_to = models.ManyToManyField(Staff, blank=True, related_name='request_assigned_staff')
    closed_on = models.DateField(blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='request_created_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField('Создана', auto_now_add=True)
    is_proceed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.priority + ': ' + self.request_type + ' - ' + self.created_by.username  # TODO: created_by.username -> что-то нормальное

    def get_assigned_staff(self):
        return Staff.objects.get(id=self.assigned_to.id)
