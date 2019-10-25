from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from requests.models import Request
from requests.forms import RequestForm
from staff.models import Staff
from clients.models import Client
from apartments.models import Apartment
from .tables import RequestTable, RequestFilter
from users.views import AdminRequiredMixin


class RequestsListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Request
    table_class = RequestTable
    template_name = "crm/list.html"
    export_name = "Zayavki"
    filterset_class = RequestFilter

    def get_context_data(self, **kwargs):
        context = super(RequestsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'requests:create',
            }
        }
        return {**context, **custom_context}


class CreateRequestView(AdminRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = "crm/create.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.assigned_to = Staff.objects.all()
        self.clients = Client.objects.all()
        self.apartments = Apartment.objects.all()

    def get_form_kwargs(self):
        kwargs = super(CreateRequestView, self).get_form_kwargs()
        kwargs.update({'assigned_to': self.assigned_to,
                       'clients': self.clients,
                       'apartments': self.apartments})
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        form.save_m2m()
        if self.request.POST.get("save_new"):
            return redirect("requests:create")
        else:
            return redirect("requests:list")

    def get_context_data(self, **kwargs):
        context = super(CreateRequestView, self).get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'requests:list',
            }
        }
        return {**context, **custom_context}


class UpdateRequestView(CreateRequestView, UpdateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        return redirect("requests:list")


class RequestDetailView(AdminRequiredMixin, DetailView):
    model = Request
    context_object_name = "request_record"
    template_name = "crm/requests/detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.assigned_to = Request.objects.all()
        return super(RequestDetailView, self).dispatch(request, *args, **kwargs)


class RemoveRequestView(AdminRequiredMixin, DeleteView):
    def get(self, request, *args, **kwargs):
        return self.post(**kwargs)

    def post(self, **kwargs):
        self.object = get_object_or_404(Request, id=kwargs.get("pk"))
        self.object.delete()
        return redirect("requests:list")
