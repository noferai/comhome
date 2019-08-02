import django_tables2 as tables
import django_filters as filters
from django.forms import widgets
from .models import Request
from staff.models import Staff


class RequestTable(tables.Table):
    created_on = tables.DateColumn(format="d.m.Y")
    assigned_to = tables.ManyToManyColumn(verbose_name="Исполнители", linkify_item=True)
    applicant = tables.Column(verbose_name="Заявитель")
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'requests:view',
        'edit_link': 'requests:edit',
        'remove_link': 'requests:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Request
        fields = ['created_on', 'applicant', 'request_type', 'assigned_to', 'priority', 'is_proceed', 'closed_on']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}


class RequestFilter(filters.FilterSet):
    created_on = filters.DateFromToRangeFilter(widget=filters.widgets.RangeWidget(attrs={'type': 'date'}))
    closed_on = filters.DateFromToRangeFilter(widget=filters.widgets.RangeWidget(attrs={'type': 'date'}))
    assigned_to = filters.ModelMultipleChoiceFilter(widget=widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                queryset=Staff.objects.all())

    class Meta:
        model = Request
        fields = ['created_on', 'request_type', 'assigned_to', 'priority', 'is_proceed', 'closed_on']
