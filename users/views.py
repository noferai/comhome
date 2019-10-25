from django.contrib.auth.mixins import LoginRequiredMixin
from ComfortableHome.mixins import AdminRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, DeleteView)
from users.forms import AdminForm
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from .tables import *


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "crm/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["user_obj"] = self.request.user
        return context


class AdminsListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Admin
    template_name = "crm/list.html"
    table_class = AdminTable
    export_name = "Polzovateli"
    filterset_class = AdminFilter

    def get_context_data(self, **kwargs):
        context = super(AdminsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'users:create',
            }
        }
        return {**context, **custom_context}


class CreateAdminView(AdminRequiredMixin, CreateView):
    model = Admin
    form_class = AdminForm
    template_name = "crm/create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        if form.cleaned_data.get("password"):
            user.set_password(form.cleaned_data.get("password"))
        user.save()

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy('users:list'), 'error': False}
            return JsonResponse(data)
        if self.request.POST.get("save_new"):
            return redirect("users:create")
        else:
            return redirect("users:list")

    def form_invalid(self, form):
        response = super(CreateAdminView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return response

    def get_context_data(self, **kwargs):
        context = super(CreateAdminView, self).get_context_data(**kwargs)
        custom_context = {
            'urls': {
                'list': 'users:list',
            }
        }
        return {**context, **custom_context}


class AdminDetailView(AdminRequiredMixin, DetailView):
    model = Admin
    context_object_name = "users"
    #   TODO: Шаблон для администратора
    template_name = "crm/users/list.html"

    def get_context_data(self, **kwargs):
        context = super(AdminDetailView, self).get_context_data(**kwargs)
        users_list = Admin.objects.all()
        context.update({
            "users": users_list, "user_obj": self.object,
            "active_users": users_list.filter(is_active=True),
            "inactive_users": users_list.filter(is_active=False)
        })
        return context


class UpdateAdminView(CreateAdminView, UpdateView):
    pass


class AdminDeleteView(AdminRequiredMixin, DeleteView):
    model = Admin

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("users:list")
