import django_tables2 as tables
import django_filters as filters
from .models import Address, Services


class AddressTable(tables.Table):
    created_date = tables.DateColumn(format="d.m.Y")
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'edit_link': 'catalog:address_edit',
        'remove_link': 'catalog:address_remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Address
        fields = ['created_date', 'address_str']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}


class AddressFilter(filters.FilterSet):
    created_date = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(AddressFilter, self).__init__(*args, **kwargs)
        self.filters['created_date'].label = 'Дата (диапазон)'

    class Meta:
        model = Services
        fields = ['created_date']


class ServicesTable(tables.Table):
    created_date = tables.DateColumn(format="d.m.Y")
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'catalog:services_detail',
        'edit_link': 'catalog:service_edit',
        'remove_link': 'catalog:service_remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Services
        fields = ['created_date', 'name_of_service', 'debt_at_beg_of_period', 'accrued', 'recalculations', 'paid',
                  'debt_at_end_of_period']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}


class ServicesFilter(filters.FilterSet):
    created_date = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(ServicesFilter, self).__init__(*args, **kwargs)
        self.filters['created_date'].label = 'Дата (диапазон)'

    class Meta:
        model = Services
        fields = ['created_date']
