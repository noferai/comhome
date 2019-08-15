import django_tables2 as tables
import django_filters as filters
from .models import Address


class AddressTable(tables.Table):
    address_str = tables.Column(verbose_name="Адрес", accessor=tables.A('__str__'),)
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'edit_link': 'catalog:address_edit',
        'remove_link': 'catalog:address_remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Address
        fields = ['address_str']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class AddressFilter(filters.FilterSet):
    created_on = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(AddressFilter, self).__init__(*args, **kwargs)
        self.filters['created_on'].label = 'Дата (диапазон)'

    class Meta:
        model = Address
        fields = ['created_on']
