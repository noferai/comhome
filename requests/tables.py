import django_tables2 as tables
import django_filters as filters
from django.forms import widgets
from .models import Request
from staff.models import Staff


class RequestTable(tables.Table):
    created_on = tables.DateColumn(format="d.m.Y")
    assigned_to = tables.ManyToManyColumn(verbose_name="Исполнители", linkify_item=True)
    applicant = tables.Column(verbose_name="Заявитель", linkify=True, accessor="applicant")
    apartment = tables.Column(verbose_name="Помещение", linkify=True)
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'requests:view',
        'edit_link': 'requests:edit',
        'remove_link': 'requests:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Request
        fields = ['created_on', 'applicant', 'request_type', 'assigned_to', 'priority', 'is_proceed', 'closed_on',
                  'apartment']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class RequestFilter(filters.FilterSet):
    created_on = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range', 'type': 'date'}))
    # closed_on = filters.DateFromToRangeFilter(widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range','type': 'date'}))
    assigned_to = filters.ModelMultipleChoiceFilter(widget=widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                    queryset=Staff.objects.all())

    def __init__(self, *args, **kwargs):
        super(RequestFilter, self).__init__(*args, **kwargs)
        self.filters['created_on'].label = 'Дата (диапазон)'
        self.filters['assigned_to'].label = 'Исполнители'

    class Meta:
        model = Request
        fields = ['created_on', 'request_type', 'assigned_to', 'priority', 'is_proceed']
