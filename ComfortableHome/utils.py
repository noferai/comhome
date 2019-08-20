from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem


class ApartmentStatusChoices(DjangoChoices):
    empty = ChoiceItem('Не заселена', _('Не заселена'))
    populated = ChoiceItem('Заселена', _('Заселена'))


class RequestTypeChoices(DjangoChoices):
    plumb = ChoiceItem('Сантехник', _('Сантехник'))
    electrical = ChoiceItem('Электрик', _('Электрик'))
    house_master = ChoiceItem('House master', _('House master'))
    cleaner = ChoiceItem('Уборщик', _('Уборщик'))
    low_voltage_master = ChoiceItem('Слаботочник', _('Слаботочник'))
    other = ChoiceItem('Прочее', _('Прочее'))


class RequestPriorityChoices(DjangoChoices):
    low = ChoiceItem('Низкая', _('Низкая'))
    medium = ChoiceItem('Средняя', _('Средняя'))
    high = ChoiceItem('Высокая', _('Высокая'))


class RequestStatusChoices(DjangoChoices):
    scheduled = ChoiceItem('Запланировано', _('Запланировано'))
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


class CityChoices(DjangoChoices):
    moscow = ChoiceItem('Москва', _('Москва'))


class PostStatusChoices(DjangoChoices):
    published = ChoiceItem(True, _('Опубликовано'))
    draft = ChoiceItem(False, _('Черновик'))


class DocumentTypeChoices(DjangoChoices):
    h1 = ChoiceItem('Заявление на застройщика', _('Заявление на застройщика'))
    h2 = ChoiceItem('АПП', _('АПП'))
    h3 = ChoiceItem('Акт осмотра', _('Акт осмотра'))
    h4 = ChoiceItem('ДУ', _('ДУ'))
    h5 = ChoiceItem('Акт приема-передачи документов и ключей', _('Акт приема-передачи документов и ключей'))
    h6 = ChoiceItem('Договор возмездного оказания услуг', _('Договор возмездного оказания услуг'))
    h7 = ChoiceItem('Соглашение об отсутствии общественного транспорта на территории ЖК',
                    _('Соглашение об отсутствии общественного транспорта на территории ЖК'))
    h8 = ChoiceItem('Согласие на обр.перс.данных', _('Согласие на обр.перс.данных'))
    h9 = ChoiceItem('Гарантийное письмо', _('Гарантийное письмо'))
    h10 = ChoiceItem('Заявление на КГМ (просто заявление, без факта оплаты)',
                     _('Заявление на КГМ (просто заявление, без факта оплаты)'))
    h11 = ChoiceItem('КГМ (ДАТА ОПЛАТЫ)', _('КГМ (ДАТА ОПЛАТЫ)'))
    h12 = ChoiceItem('Соглашение о компенсации', _('Соглашение о компенсации'))
