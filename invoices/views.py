from django.shortcuts import redirect
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView)
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from users.views import AdminRequiredMixin
from .tables import *
from .forms import *


class InvoiceListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Invoice
    table_class = InvoiceTable
    template_name = "crm/list.html"
    export_name = "Servisy"
    filterset_class = InvoiceFilter

    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'invoices:create',
            }
        }
        return {**context, **custom_context}


class InvoiceAddView(AdminRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "crm/create.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        service_object = form.save(commit=False)
        service_object.created_by = self.request.user
        service_object.save()
        if self.request.POST.get("save_new"):
            return redirect("invoices:create")
        else:
            return redirect("invoices:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(InvoiceAddView, self).get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'invoices:list',
            }
        }
        return {**context, **custom_context}


class InvoiceEditView(InvoiceAddView, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        account_object = form.save(commit=False)
        account_object.save()
        return redirect("catalog:invoices_list")


class InvoiceDeleteView(AdminRequiredMixin, DeleteView):
    model = Invoice

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("catalog:invoices_list")

#   Todo: Карточка взаиморасчета
# class InvoiceDetailView(AdminRequiredMixin, DetailView):
#     model = Invoice
#     context_object_name = "service"
#     template_name = "crm/catalog/detail_list.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         self.service = Invoice.objects.all()
#         return super(InvoiceDetailView, self).dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(InvoiceDetailView, self).get_context_data(**kwargs)
#         return context

