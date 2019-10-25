from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView, UpdateView, DetailView, DeleteView)
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from staff.forms import StaffForm
from staff.models import Staff
from users.models import User
from .tables import StaffTable, StaffFilter
from users.views import AdminRequiredMixin


class StaffListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Staff
    table_class = StaffTable
    template_name = "crm/list.html"
    export_name = "Ispolniteli"
    filterset_class = StaffFilter

    def get_context_data(self, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'staff:create',
            }
        }
        return {**context, **custom_context}


class CreateStaffView(AdminRequiredMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = "crm/create.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        if self.request.POST.get("save_new"):
            return redirect("staff:create")
        else:
            return redirect("staff:list")

    def get_context_data(self, **kwargs):
        context = super(CreateStaffView, self).get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'staff:list',
            }
        }
        return {**context, **custom_context}


class StaffDetailView(AdminRequiredMixin, DetailView):
    model = Staff
    context_object_name = "staff"
    template_name = "crm/staff/detail.html"


class StaffUpdateView(CreateStaffView, UpdateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return redirect("staff:list")


class StaffDeleteView(AdminRequiredMixin, DeleteView):
    model = Staff

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("staff:list")