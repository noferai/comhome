import django_tables2 as tables
import django_filters as filters
from .models import Poll


class PollsTable(tables.Table):
    # actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
    #     # 'view_link': 'invoices:view',
    #     'edit_link': 'invoices:edit',
    #     'remove_link': 'invoices:remove'
    # }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Poll
        fields = ['created_on', 'question']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class PollFilter(filters.FilterSet):
    created_on = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(PollFilter, self).__init__(*args, **kwargs)
        self.filters['created_on'].label = 'Дата (диапазон)'

    class Meta:
        model = Poll
        fields = ['created_on',]
