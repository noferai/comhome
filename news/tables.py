import django_tables2 as tables
import django_filters as filters
from django.forms import widgets
from .models import Entry
from common.models import User


class EntryTable(tables.Table):
    created_date = tables.DateColumn(format="d.m.Y")
    author = tables.Column(verbose_name="Автор", linkify=True, accessor="author")
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'view_link': 'news:view',
        'edit_link': 'news:edit',
        'remove_link': 'news:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = Entry
        fields = ['created_date', 'author', 'is_published']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}


class EntryFilter(filters.FilterSet):
    created_date = filters.DateFromToRangeFilter(widget=filters.widgets.RangeWidget(attrs={'type': 'date'}))
    author = filters.ModelMultipleChoiceFilter(widget=widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                queryset=User.objects.all())

    class Meta:
        model = Entry
        fields = ['created_date', 'author', 'is_published']
