from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Address
from .forms import AddressForm
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .tables import AddressTable, AddressFilter
from users.views import AdminRequiredMixin


class AddressesListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Address
    table_class = AddressTable
    template_name = "crm/list.html"
    export_name = "Adresa"
    filterset_class = AddressFilter

    def get_context_data(self, **kwargs):
        context = super(AddressesListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'addresses:create',
            }
        }
        return {**context, **custom_context}


class AddressAddView(AdminRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = "crm/create.html"

    def form_valid(self, form):
        self.object = form.save()
        if self.request.POST.get("save_new"):
            return redirect("addresses:create")
        else:
            return redirect("addresses:list")

    def get_context_data(self, **kwargs):
        context = super(AddressAddView, self).get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'addresses:list',
            }
        }
        return {**context, **custom_context}


class AddressEditView(AddressAddView, UpdateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return redirect("addresses:list")


class AddressDeleteView(AdminRequiredMixin, DeleteView):
    model = Address

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("addresses:list")
