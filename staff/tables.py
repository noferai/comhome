import django_tables2 as tables
import django_filters as filters
from .models import Staff


class StaffTable(tables.Table):
    created_on = tables.DateColumn(format="d.m.Y")
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'staff:view',
        'edit_link': 'staff:edit',
        'remove_link': 'staff:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Staff
        fields = ['created_on', 'name', 'industry', 'phone', 'is_active']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}


class StaffFilter(filters.FilterSet):
    created_on = filters.DateFromToRangeFilter(widget=filters.widgets.RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Staff
        fields = ['created_on', 'name', 'industry', 'phone', 'is_active']
