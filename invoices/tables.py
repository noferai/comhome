import django_tables2 as tables
import django_filters as filters
from .models import Invoice


class InvoiceTable(tables.Table):
    created_on = tables.DateColumn(format="d.m.Y")
    number_of_business_account = tables.Column(verbose_name="ЛС", accessor="apartment.number_of_business_account")
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        # 'view_link': 'invoices:view',
        'edit_link': 'invoices:edit',
        'remove_link': 'invoices:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Invoice
        fields = ['created_on', 'number_of_business_account', 'name', 'accrued', 'paid']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class InvoiceFilter(filters.FilterSet):
    created_on = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range date'}))

    def __init__(self, *args, **kwargs):
        super(InvoiceFilter, self).__init__(*args, **kwargs)
        self.filters['created_on'].label = 'Дата (диапазон)'

    class Meta:
        model = Invoice
        fields = ['created_on']
