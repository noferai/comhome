import django_tables2 as tables
import django_filters as filters
from .models import Staff


class StaffTable(tables.Table):
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'staff:view',
        'edit_link': 'staff:edit',
        'remove_link': 'staff:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Staff
        fields = ['name', 'occupation', 'phone', 'is_active']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class StaffFilter(filters.FilterSet):
    class Meta:
        model = Staff
        fields = ['occupation', 'is_active']
