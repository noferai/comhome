from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    CreateView, UpdateView,  TemplateView, DeleteView)
from catalog.models import Address
from catalog.forms import AddressForm


class AddressesListView(LoginRequiredMixin, TemplateView):
    model = Address
    context_object_name = "addresses_list"
    template_name = "catalog/list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AddressesListView, self).get_context_data(**kwargs)
        context["addresses_list"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


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


class AddressEditView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "catalog/create.html"

    def get_form_kwargs(self):
        kwargs = super(AddressEditView, self).get_form_kwargs()
        return kwargs

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

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(AddressEditView, self).get_context_data(**kwargs)
        context["address_obj"] = self.object
        context["address_form"] = context["form"]
        return context


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'catalog/list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("catalog:addresses_list")