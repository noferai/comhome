from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem


class ApartmentStatusChoices(DjangoChoices):
    empty = ChoiceItem('Не заселена', _('Не заселена'))
    populated = ChoiceItem('Заселена', _('Заселена'))


class RequestTypeChoices(DjangoChoices):
    plumb = ChoiceItem('Сантехника', _('Сантехника'))
    electrical = ChoiceItem('Эллектрик', _('Эллектрик'))
    house_master = ChoiceItem('House master', _('House master'))
    cleaner = ChoiceItem('Уборщик', _('Уборщик'))
    low_voltage_master = ChoiceItem('Слаботочник', _('Слаботочник'))
    other = ChoiceItem('Прочее', _('Прочее'))


class RequestPriorityChoices(DjangoChoices):
    low = ChoiceItem('Низкая', _('Низкая'))
    medium = ChoiceItem('Средняя', _('Средняя'))
    high = ChoiceItem('Высокая', _('Высокая'))


class RequestStatusChoices(DjangoChoices):
    scheduled = ChoiceItem('Запланированно', _('Запланированно'))
    new = ChoiceItem('Новая', _('Новая'))
    processed = ChoiceItem('В работе', _('В работе'))
    closed = ChoiceItem('Завершено', _('Завершено'))
    rejected = ChoiceItem('Отменено', _('Отменено'))


class StaffOccupationChoices(DjangoChoices):
    electrical = ChoiceItem('Электрик', _('Электрик'))
    plumb = ChoiceItem('Сантехник', _('Сантехник'))
    locksmith = ChoiceItem('Слесарь', _('Слесарь'))
    low_voltage_master = ChoiceItem('Слаботочник', _('Слаботочник'))
    security = ChoiceItem('Охранник', _('Охранник'))


class OrganizationChoices(DjangoChoices):
    admiral = ChoiceItem('AD', _('ООО «УК АДМИРАЛ»'))
    alyans = ChoiceItem('AL', _('ООО «УК АЛЬЯНС»'))
