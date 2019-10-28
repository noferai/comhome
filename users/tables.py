import django_tables2 as tables
import django_filters as filters
from .models import Admin


class AdminTable(tables.Table):
    date_joined = tables.DateColumn(format="d.m.Y")
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'users:view',
        'edit_link': 'users:edit',
        'remove_link': 'users:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Admin
        fields = ['date_joined', 'name', 'email', 'is_active']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"


class AdminFilter(filters.FilterSet):
    date_joined = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range date'}))

    def __init__(self, *args, **kwargs):
        super(AdminFilter, self).__init__(*args, **kwargs)
        self.filters['date_joined'].label = 'Дата (диапазон)'

    class Meta:
        model = Admin
        fields = ['date_joined']
