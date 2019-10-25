from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem


class ClientTypeChoices(DjangoChoices):
    individual = ChoiceItem('Физ. лицо', _('Физ. лицо'))
    entity = ChoiceItem('Юр. лицо', _('Юр. лицо'))


class ClientGenderChoices(DjangoChoices):
    male = ChoiceItem('Мужской', _('Мужской'))
    female = ChoiceItem('Женский', _('Женский'))
    none = ChoiceItem('Не указан', _('Не указан'))


class ApartmentTypeChoices(DjangoChoices):
    residential = ChoiceItem('Жилое', _('Жилое'))
    non_residential = ChoiceItem('Нежилое', _('Нежилое'))


class ApartmentStatusChoices(DjangoChoices):
    empty = ChoiceItem('Не заселена', _('Не заселена'))
    occupied = ChoiceItem('Заселена', _('Заселена'))


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
    h2 = ChoiceItem('Акт осмотра', _('Акт осмотра'))
    h3 = ChoiceItem('Акт приема-передачи документов и ключей', _('Акт приема-передачи документов и ключей'))
    h4 = ChoiceItem('Договор возмездного оказания услуг', _('Договор возмездного оказания услуг'))
    h5 = ChoiceItem('Соглашение об отсутствии общественного транспорта на территории ЖК',
                    _('Соглашение об отсутствии общественного транспорта на территории ЖК'))
    h6 = ChoiceItem('Согласие на обр.перс.данных', _('Согласие на обр.перс.данных'))
    h7 = ChoiceItem('Гарантийное письмо', _('Гарантийное письмо'))
