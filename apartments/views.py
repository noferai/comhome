from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import (CreateView, UpdateView, DetailView, DeleteView)
from apartments.forms import ApartmentForm, DocumentFormSet
from apartments.models import Apartment
from requests.models import Request
from addresses.models import Address
from invoices.models import Invoice
from documents.models import Document
from documents.tables import DocumentTable
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .tables import ApartmentTable, ApartmentFilter, ApartmentRequestTable, ApartmentInvoiceTable
from users.views import AdminRequiredMixin


class ApartmentListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Apartment
    table_class = ApartmentTable
    template_name = "crm/list.html"
    export_name = "Kvartiry"
    filterset_class = ApartmentFilter

    def get_context_data(self, **kwargs):
        context = super(ApartmentListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'apartments:create',
            }
        }
        return {**context, **custom_context}


class ApartmentAddView(AdminRequiredMixin, CreateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = "crm/create.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.addresses = Address.objects.all()

    def get_form_kwargs(self):
        kwargs = super(ApartmentAddView, self).get_form_kwargs()
        kwargs.update({"addresses": self.addresses})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        if self.request.POST.get("save_new"):
            return redirect("apartments:create")
        else:
            return redirect("apartments:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ApartmentAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DocumentFormSet(self.request.POST, self.request.FILES or None)
        else:
            context['formset'] = DocumentFormSet()
        custom_context = {
            'formset_prefix': 'documents',
            'formset_title': 'Документы',
            'urls': {
                'list': 'apartments:list',
            }
        }
        return {**context, **custom_context}


class ApartmentEditView(AdminRequiredMixin, UpdateView):
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
        return redirect("apartments:list")


class ApartmentDetailView(AdminRequiredMixin, DetailView):
    model = Apartment
    context_object_name = "apartment"
    template_name = "crm/apartments/detail.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.addresses = Address.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ApartmentDetailView, self).get_context_data(**kwargs)
        context.update({'requests_table': ApartmentRequestTable(Request.objects.filter(apartment__id=self.object.id)),
                        'invoices_table': ApartmentInvoiceTable(Invoice.objects.filter(apartment__id=self.object.id)),
                        'documents_table': DocumentTable(Document.objects.filter(apartment__id=self.object.id))
                        })
        return context


class ApartmentDeleteView(AdminRequiredMixin, DeleteView):
    model = Apartment

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("apartments:list")
