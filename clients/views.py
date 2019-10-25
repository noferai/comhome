from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView, View
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from apartments.models import Apartment
from documents.models import Document
from requests.models import Request
from .models import Client
from .forms import ClientForm, PhoneFormSet, DocumentFormSet
from .tables import ClientTable, ClientFilter, ClientRequestTable
from documents.tables import DocumentTable
from users.views import AdminRequiredMixin


class ClientListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Client
    table_class = ClientTable
    template_name = "crm/list.html"
    export_name = "Sobstvenniki"
    filterset_class = ClientFilter

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'clients:create',
            }
        }
        return {**context, **custom_context}


class CreateClientView(AdminRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "crm/create.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apartments = Apartment.objects.all()

    def get_form_kwargs(self):
        kwargs = super(CreateClientView, self).get_form_kwargs()
        kwargs.update({'apartments': self.apartments})
        return kwargs

    def form_valid(self, form):
        formsets = self.get_context_data()['formsets']
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        if self.apartments.count() > 0:
            form.save_m2m()
        for formset in formsets:
            with transaction.atomic():
                self.object = form.save()
                if formset['form'].is_valid():
                    formset['form'].instance = self.object
                    formset['form'].save()
        if self.request.POST.get("save_new"):
            return redirect("clients:create")
        else:
            return redirect('clients:list')

    def get_context_data(self, **kwargs):
        context = super(CreateClientView, self).get_context_data(**kwargs)
        formsets = []
        if self.request.POST:
            formsets.append({'form': PhoneFormSet(self.request.POST),
                             'title': 'Контактные номера',
                             'prefix': 'phones'
                             })
            formsets.append({'form': DocumentFormSet(self.request.POST, self.request.FILES or None),
                             'title': 'Документы',
                             'prefix': 'documents'
                             })
        else:
            formsets.append({'form': PhoneFormSet(),
                             'title': 'Контактные номера',
                             'prefix': 'phones'
                             })
            formsets.append({'form': DocumentFormSet(),
                             'title': 'Документы',
                             'prefix': 'documents'
                             })
        custom_context = {
            'formsets': formsets,
            'urls': {
                'list': 'clients:list',
            }
        }
        return {**context, **custom_context}


class UpdateClientView(CreateClientView, UpdateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        return redirect('clients:list')


class ClientDetailView(AdminRequiredMixin, DetailView):
    model = Client
    context_object_name = "client"
    template_name = "crm/clients/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context.update({
            'requests_table': ClientRequestTable(Request.objects.filter(applicant__id=self.object.id)),
            'documents_table': DocumentTable(Document.objects.filter(apartment__id=self.object.id))
        })
        return context


class DeleteClientView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(**kwargs)

    def post(self, **kwargs):
        self.object = get_object_or_404(Client, id=kwargs.get("pk"))
        self.object.delete()
        return redirect("clients:list")
