import django_tables2 as tables
import django_filters as filters
from django.forms import widgets
from .models import Apartment
from catalog.models import Address
from homeowners.models import Homeowner
from requests.tables import RequestTable


class ApartmentTable(tables.Table):
    created_date = tables.DateColumn(format="d.m.Y")
    address = tables.Column(verbose_name="Адрес")
    homeowner = tables.ManyToManyColumn(verbose_name="Собственники", linkify_item=True)
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'apartments:view',
        'edit_link': 'apartments:edit',
        'remove_link': 'apartments:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Apartment
        fields = ['created_date', 'address', 'apartment_number', 'area', 'homeowner']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}


class ApartmentFilter(filters.FilterSet):
    created_date = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range', 'type': 'date'}))
    address = filters.ModelMultipleChoiceFilter(widget=widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                queryset=Address.objects.all())
    homeowner = filters.ModelMultipleChoiceFilter(widget=widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                  queryset=Homeowner.objects.all())

    def __init__(self, *args, **kwargs):
        super(ApartmentFilter, self).__init__(*args, **kwargs)
        self.filters['created_date'].label = 'Дата (диапазон)'
        self.filters['address'].label = 'Адреса'
        self.filters['homeowner'].label = 'Собственники'

    class Meta:
        model = Apartment
        fields = ['created_date', 'address', 'homeowner']


class ApartmentRequestTable(RequestTable):
    class Meta:
        exclude = ['apartment']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
