from django.db import models
from django.urls import reverse
from users.models import User


class Entry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=2000)
    text = models.TextField('Текст')
    is_published = models.BooleanField('Опубликовано', default=True)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_on']
