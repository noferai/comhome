import django_tables2 as tables
import django_filters as filters
from django.forms import widgets
from .models import Client
from apartments.models import Apartment
from requests.tables import RequestTable


class ClientTable(tables.Table):
    date_joined = tables.DateColumn(format="d.m.Y")
    apartments = tables.ManyToManyColumn(verbose_name="Помещения", linkify_item=True)
    phones = tables.TemplateColumn(verbose_name="Телефоны", orderable=False,
                                   template_code='''
                                        {% for val in value %}
                                            {{ val }}{% if not forloop.last %},<br>{% endif %}
                                        {%endfor%}
                                        ''', accessor='client.phones.all')
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'clients:view',
        'edit_link': 'clients:edit',
        'remove_link': 'clients:remove'
    }, orderable=False, exclude_from_export=True)

    #
    # def render_phones(self, value):
    #     return [value.first(), value.last()]

    class Meta:
        model = Client
        fields = ['date_joined', 'name', 'phones', 'apartments']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class ClientFilter(filters.FilterSet):
    created_on = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range', 'type': 'date'}))
    apartments = filters.ModelMultipleChoiceFilter(widget=widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                   queryset=Apartment.objects.all())

    def __init__(self, *args, **kwargs):
        super(ClientFilter, self).__init__(*args, **kwargs)
        self.filters['date_joined'].label = 'Дата (диапазон)'
        self.filters['apartments'].label = 'Помещения'

    class Meta:
        model = Client
        fields = ['date_joined', 'apartments']


class ClientRequestTable(RequestTable):
    class Meta(RequestTable.Meta):
        exclude = ['applicant']

