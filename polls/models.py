from django.db import models
from users.models import Admin
from ComfortableHome.utils import PostStatusChoices


class Poll(models.Model):
    question = models.CharField("Вопрос", max_length=200)
    status = models.BooleanField('Статус', choices=PostStatusChoices.choices, default=PostStatusChoices.draft)
    created_by = models.ForeignKey(Admin, related_name='poll_created_by', null=True, on_delete=models.SET_NULL)
    created_on = models.DateField('Создано', auto_now_add=True)
    modified_on = models.DateField('Изменено', auto_now=True)
    # start_date
    # end_date

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Choice(models.Model):
    poll = models.ForeignKey(Poll, null=True, on_delete=models.CASCADE)
    choice_text = models.CharField("Вариант ответа", max_length=200)
    votes = models.IntegerField("Голоса", default=0)

    def __str__(self):
        return self.choice_text
