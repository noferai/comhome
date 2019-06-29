from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem


class RequestPriorityChoices(DjangoChoices):
    male = ChoiceItem('Мужской', _('Мужской'))
    female = ChoiceItem('Женский', _('Женский'))

