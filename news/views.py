from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, DeleteView)
from django.shortcuts import redirect
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .forms import EntryForm
from .tables import EntryTable, EntryFilter
from users.views import AdminRequiredMixin
from news.models import Entry
from rest_framework.views import APIView
from rest_framework.response import Response
from news.serializer import EntrySerializer
import textwrap
import json


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

    def get_form_kwargs(self):
        kwargs = super(CreateEntryView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(form_class=EntryForm)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user     # User model object instance
        instance.save()
        if self.request.POST.get("save_new"):
            return redirect("news:create")
        else:
            return redirect("news:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'news:list',
            }
        }
        return {**context, **custom_context}


class EntryUpdateView(CreateEntryView, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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

