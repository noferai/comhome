import django_tables2 as tables
import django_filters as filters
from django.forms import widgets
from .models import Apartment
from addresses.models import Address
from homeowners.models import Homeowner
from requests.tables import RequestTable
from invoices.tables import InvoiceTable
from documents.tables import DocumentTable


class ApartmentTable(tables.Table):
    address = tables.Column(verbose_name="Адрес")
    balance_of_business_account = tables.Column(verbose_name="Баланс")
    number_of_business_account = tables.Column(verbose_name="ЛС")
    homeowner = tables.ManyToManyColumn(verbose_name="Собственники", linkify_item=True)
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'apartments:view',
        # TODO: Не работает. Починить
        # 'edit_link': 'apartments:edit',
        'remove_link': 'apartments:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Apartment
        fields = ['number_of_business_account', 'address', 'apartment_number', 'area', 'homeowner',
                  'balance_of_business_account']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class ApartmentFilter(filters.FilterSet):
    address = filters.ModelMultipleChoiceFilter(widget=widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                queryset=Address.objects.all(), label='Адреса')
    homeowner = filters.ModelMultipleChoiceFilter(widget=widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                  queryset=Homeowner.objects.all(), label='Собственники')

    class Meta:
        model = Apartment
        fields = ['address', 'homeowner']


class ApartmentRequestTable(RequestTable):
    class Meta(RequestTable.Meta):
        exclude = ['apartment']


class ApartmentInvoiceTable(InvoiceTable):
    class Meta(InvoiceTable.Meta):
        exclude = ['apartment']

