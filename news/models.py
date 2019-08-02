from django.db import models
from django.urls import reverse
from common.models import User
from django.utils import timezone


class Entry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=2000)
    text = models.TextField('Текст')
    created_date = models.DateField('Дата', default=timezone.now)
    published_date = models.DateField('Дата публикации', blank=True, null=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
