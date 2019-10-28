import django_tables2 as tables
from .models import PhoneNumber


class PhoneTable(tables.Table):
    actions = tables.TemplateColumn(verbose_name="Действия", template_name="misc/linkbuttons.html", extra_context={
        'edit_link': 'phones:edit',
        'remove_link': 'phones:remove'
    }, orderable=False, exclude_from_export=True)

    class Meta:
        model = PhoneNumber
        fields = ['number', 'note']
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped table-bordered text-center'}
        empty_text = "Ничего не найдено"
