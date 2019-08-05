import django_tables2 as tables
import django_filters as filters
from .models import User


class UserTable(tables.Table):
    date_joined = tables.DateColumn(format="d.m.Y")
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'common:view_user',
        'edit_link': 'common:edit_user',
        'remove_link': 'common:remove_user'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = User
        fields = ['date_joined', 'first_name', 'last_name', 'email', 'is_active', 'is_admin']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}


class UserFilter(filters.FilterSet):
    date_joined = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(attrs={'class': 'form-control date-range', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(UserFilter, self).__init__(*args, **kwargs)
        self.filters['date_joined'].label = 'Дата (диапазон)'

    class Meta:
        model = User
        fields = ['date_joined']
