from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem


class RequestChoicesGender(DjangoChoices):
    male = ChoiceItem('Мужской', _('Мужской'))
    female = ChoiceItem('Женский', _('Женский'))


class RequestChoicesDebtStatus(DjangoChoices):
    first = ChoiceItem('Не начата', _('Не начата'))
    second = ChoiceItem('В процессе', _('В процессе'))


class RequestChoicesGarbagePayment(DjangoChoices):
    paid = ChoiceItem(True, _('Оплачено'))
    no = ChoiceItem(False, _('Нет'))


class RequestChoicesTypePassport(DjangoChoices):
    usual = ChoiceItem('РФ', _('РФ'))
    overseas = ChoiceItem('Заграничный', _('Заграничный'))
