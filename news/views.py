from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, DeleteView)
from django.shortcuts import redirect
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .forms import EntryForm
from .tables import EntryTable, EntryFilter

from rest_framework.views import APIView
from rest_framework.response import Response

from news.models import Entry
from news.serializer import EntrySerializer
import textwrap
import json


class NewsListView(LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Entry
    table_class = EntryTable
    template_name = "list.html"
    export_name = "Novosti"
    filterset_class = EntryFilter

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'news:add',
            }
        }
        return {**context, **custom_context}


class CreateEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "news/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.news = Entry.objects.filter(is_published=True).order_by('published_date')
        return super(CreateEntryView, self).dispatch(request, *args, **kwargs)

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
        entry_object = form.save(commit=False)
        entry_object.author = self.request.user     # User model object instance
        entry_object.save()
        if self.request.POST.get("savenewform"):
            return redirect("news:add")
        else:
            return redirect("news:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_context = {
            'entry_form': context["form"],
            'news_list': self.news,
        }
        return {**context, **custom_context}


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    context_object_name = "entry_record"
    template_name = "news/detail.html"

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        custom_context = {
            'entry_form': context["entry_record"],
        }

        return {**context, **custom_context}


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "news/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.news = Entry.objects.filter(is_published=True).order_by('published_date')
        return super(EntryUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        entry_object = form.save(commit=False)
        entry_object.save()
        if self.request.POST.get("savenewform"):
            return redirect("news:add")
        else:
            return redirect("news:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_context = {
            'enrty_obj': self.object,
            'entry_form': context["form"],
            'news_list': self.news,
        }
        return {**context, **custom_context}


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'news/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("news:list")

