import django_tables2 as tables
import django_filters as filters
from .models import Document


class DocumentTable(tables.Table):
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'edit_link': 'documents:edit',
        'remove_link': 'documents:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Document
        fields = ['date', 'type', 'attachment', 'note']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class DocumentFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range date'}))

    def __init__(self, *args, **kwargs):
        super(DocumentFilter, self).__init__(*args, **kwargs)
        self.filters['date'].label = 'Дата (диапазон)'

    class Meta:
        model = Document
        fields = ['date']
