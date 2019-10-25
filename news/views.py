from django.views.generic import (
    CreateView, UpdateView, DetailView, DeleteView)
from django.shortcuts import redirect
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .forms import EntryForm
from .tables import EntryTable, EntryFilter
from users.views import AdminRequiredMixin
from news.models import Entry


class NewsListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Entry
    table_class = EntryTable
    template_name = "crm/list.html"
    export_name = "Novosti"
    filterset_class = EntryFilter

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'news:create',
            }
        }
        return {**context, **custom_context}


class CreateEntryView(AdminRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "crm/create.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        if self.request.POST.get("save_new"):
            return redirect("news:create")
        else:
            return redirect("news:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'news:list',
            }
        }
        return {**context, **custom_context}


class EntryUpdateView(CreateEntryView, UpdateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        if self.request.POST.get("savenewform"):
            return redirect("news:create")
        else:
            return redirect("news:list")


class EntryDetailView(AdminRequiredMixin, DetailView):
    model = Entry
    context_object_name = "entry_record"
    template_name = "crm/news/detail.html"

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        custom_context = {
            'entry_form': context["entry_record"],
        }

        return {**context, **custom_context}


class EntryDeleteView(AdminRequiredMixin, DeleteView):
    model = Entry

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("news:list")

