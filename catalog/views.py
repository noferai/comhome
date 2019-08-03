from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView)
from catalog.models import Address, Services
from catalog.forms import AddressForm, ServicesForm
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .tables import AddressTable, AddressFilter, ServicesTable, ServicesFilter


class AddressesListView(LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Address
    table_class = AddressTable
    template_name = "list.html"
    export_name = "Adresa"
    filterset_class = AddressFilter

    def get_context_data(self, **kwargs):
        context = super(AddressesListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'catalog:address_add',
            }
        }
        return {**context, **custom_context}


class AddressAddView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = "catalog/create.html"

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        address_object = form.save(commit=False)
        address_object.created_by = self.request.user
        address_object.save()
        if self.request.POST.get("savenewform"):
            return redirect("catalog:address_add")
        else:
            return redirect("catalog:addresses_list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(AddressAddView, self).get_context_data(**kwargs)
        context["address_form"] = context["form"]
        return context


class AddressEditView(AddressAddView, UpdateView):
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
        return redirect("catalog:addresses_list")


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("catalog:addresses_list")


class ServicesListView(LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Services
    table_class = ServicesTable
    template_name = "list.html"
    export_name = "Servisy"
    filterset_class = ServicesFilter

    def get_context_data(self, **kwargs):
        context = super(ServicesListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'catalog:service_add',
            }
        }
        return {**context, **custom_context}


class ServiceAddView(LoginRequiredMixin, CreateView):
    model = Services
    form_class = ServicesForm
    template_name = "catalog/create_service.html"

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
        if self.request.POST.get("savenewform"):
            return redirect("catalog:service_add")
        else:
            return redirect("catalog:services_list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ServiceAddView, self).get_context_data(**kwargs)
        context["service_form"] = context["form"]
        return context


class ServiceEditView(ServiceAddView, UpdateView):
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
        return redirect("catalog:services_list")


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Services

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("catalog:services_list")


class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Services
    context_object_name = "service"
    template_name = "catalog/detail_list.html"

    def dispatch(self, request, *args, **kwargs):
        self.service = Services.objects.all()
        return super(ServiceDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        return context
