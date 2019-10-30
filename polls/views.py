from django.db import transaction
from django.shortcuts import redirect
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django.views.generic import CreateView
from ComfortableHome.mixins import AdminRequiredMixin
from .models import Poll
from .tables import PollsTable, PollFilter
from .forms import PollForm, ChoiceFormSet


class PollsListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Poll
    table_class = PollsTable
    template_name = "crm/list.html"
    export_name = "Oprosy"
    filterset_class = PollFilter

    def get_context_data(self, **kwargs):
        context = super(PollsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'polls:create',
            }
        }
        return {**context, **custom_context}


class PollCreateView(CreateView):
    model = Poll
    form_class = PollForm
    template_name = "crm/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        formsets = []
        if self.request.POST:
            formsets.append({'form': ChoiceFormSet(self.request.POST),
                             'title': 'Варианты ответов',
                             'prefix': 'choices'})
        else:
            formsets.append({'form': ChoiceFormSet(),
                             'title': 'Варианты ответов',
                             'prefix': 'choices'})
        custom_context = {
            'formsets': formsets,
            'urls': {
                'list': 'polls:list',
            }
        }
        return {**context, **custom_context}

    def form_valid(self, form):
        formsets = self.get_context_data()['formsets']
        with transaction.atomic():
            self.object = form.save()
            for formset in formsets:
                if formset['form'].is_valid():
                    formset['form'].instance = self.object
                    formset['form'].save()
        if self.request.POST.get("save_new"):
            return redirect("polls:create")
        else:
            return redirect("polls:list")
