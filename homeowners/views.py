from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView, View
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from apartments.models import Apartment
from requests.models import Request
from .models import Homeowner
from .forms import HomeownerForm, PhoneFormSet
from .tables import HomeownerTable, HomeownerFilter, HomeownerRequestTable
from users.views import AdminRequiredMixin


class HomeownerListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Homeowner
    table_class = HomeownerTable
    template_name = "crm/list.html"
    export_name = "Sobstvenniki"
    filterset_class = HomeownerFilter

    def get_context_data(self, **kwargs):
        context = super(HomeownerListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'homeowners:create',
            }
        }
        return {**context, **custom_context}


class CreateHomeownerView(AdminRequiredMixin, CreateView):
    model = Homeowner
    form_class = HomeownerForm
    template_name = "crm/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.apartments = Apartment.objects.all()
        return super(CreateHomeownerView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateHomeownerView, self).get_form_kwargs()
        kwargs.update({"apartments": self.apartments})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        if self.apartments.count() > 0:
            form.save_m2m()
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        if self.request.POST.get("save_new"):
            return redirect("homeowners:create")
        else:
            return redirect('homeowners:list')

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateHomeownerView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhoneFormSet(self.request.POST)
        else:
            context['formset'] = PhoneFormSet()
        custom_context = {
            'formset_prefix': 'phones',
            'formset_title': 'Контактные телефоны',
            'urls': {
                'list': 'homeowners:list',
            }
        }
        return {**context, **custom_context}


class UpdateHomeownerView(CreateHomeownerView, UpdateView):
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
        form.save_m2m()
        return redirect('homeowners:list')


class HomeownerDetailView(AdminRequiredMixin, DetailView):
    model = Homeowner
    context_object_name = "homeowner"
    template_name = "crm/homeowners/detail.html"

    def get_context_data(self, **kwargs):
        context = super(HomeownerDetailView, self).get_context_data(**kwargs)
        context.update({
            "table": HomeownerRequestTable(Request.objects.filter(applicant__id=self.object.id))})
        return context


class DeleteHomeownerView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(**kwargs)

    def post(self, **kwargs):
        self.object = get_object_or_404(Homeowner, id=kwargs.get("pk"))
        self.object.delete()
        return redirect("homeowners:list")
