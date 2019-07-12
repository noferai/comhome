from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem


class ApartmentStatusChoices(DjangoChoices):
    empty = ChoiceItem('Не заселена', _('Не заселена'))
    populated = ChoiceItem('Заселена', _('Заселена'))


class RequestTypeChoices(DjangoChoices):
    electrical = ChoiceItem('Электрооборудование', _('Электрооборудование'))
    plumb = ChoiceItem('Сантехника', _('Сантехника'))
    cleaner = ChoiceItem('Уборщик', _('Уборщик'))
    other = ChoiceItem('Прочее', _('Прочее'))


class RequestPriorityChoices(DjangoChoices):
    urgent = ChoiceItem('Срочная', _('Срочная'))
    normal = ChoiceItem('Обычная', _('Обычная'))


class RequestStatusChoices(DjangoChoices):
    new = ChoiceItem('Новая', _('Новая'))
    processed = ChoiceItem('Выполняется', _('Выполняется'))
    closed = ChoiceItem('Закрыта', _('Закрыта'))
    rejected = ChoiceItem('Отклонена', _('Отклонена'))
    duplicated = ChoiceItem('Дубликат', _('Дубликат'))


class StaffOccupationChoices(DjangoChoices):
    electrical = ChoiceItem('Электрик', _('Электрик'))
    plumb = ChoiceItem('Сантехник', _('Сантехник'))
    locksmith = ChoiceItem('Слесарь', _('Слесарь'))
    security = ChoiceItem('Охранник', _('Охранник'))
