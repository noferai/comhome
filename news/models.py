from django.db import models
# TODO: в частности тут про добавление автора
from django.conf import settings
from django.utils import timezone


class Entry(models.Model):
    # TODO: добавить автоматическое добавление автора для записи новостей
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.CharField(max_length=20)

    # TODO: уточнить на счёт структуы новости
    title = models.CharField(max_length=200)

    text = models.TextField()
    created_data = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

