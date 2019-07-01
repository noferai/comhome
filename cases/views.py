from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView, View, DeleteView

from rest_framework.views import APIView
from rest_framework.response import Response

from cases.models import Case
from cases.forms import CaseForm
from common.models import Team
from accounts.models import Account

from common.utils import RequestTypeChoices, RequestPriorityChoices, RequestStatusChoices


class RequestsListView(LoginRequiredMixin, TemplateView):
    model = Case
    context_object_name = "requests"
    template_name = "requests.html"

    def get_queryset(self):
        queryset = self.model.objects.all()  # Хуйня какая-то блядская
        #print(queryset.last().assigned_to.all())
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RequestsListView, self).get_context_data(**kwargs)
        context["requests"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        context["request_type"] = RequestTypeChoices.choices
        context["request_priority"] = RequestPriorityChoices.choices
        context["request_status"] = RequestStatusChoices.choices
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateRequestView(LoginRequiredMixin, CreateView):
    model = Case
    form_class = CaseForm
    template_name = "create_request.html"

    def dispatch(self, request, *args, **kwargs):
        self.assigned_to = Account.objects.all()
        return super(CreateRequestView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateRequestView, self).get_form_kwargs()
        kwargs.update({"assigned_to": self.assigned_to})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        case = form.save(commit=False)
        case.created_by = self.request.user
        case.save()
        form.save_m2m()         # Важная хуйня
        if self.request.POST.get("savenewform"):
            return redirect("cases:create_request")
        else:
            return redirect("cases:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateRequestView, self).get_context_data(**kwargs)
        context["case_form"] = context["form"]
        context["request_types"] = RequestTypeChoices.choices
        context["request_priority"] = RequestPriorityChoices.choices
        context["request_status"] = RequestStatusChoices.choices
        return context


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Case
    context_object_name = "request_record"
    template_name = "view_request.html"

    def dispatch(self, request, *args, **kwargs):
        self.assigned_to = Case.objects.all()
        return super(RequestDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequestDetailView, self).get_context_data(**kwargs)
        return context


class UpdateRequestView(LoginRequiredMixin, UpdateView):
    model = Case
    form_class = CaseForm
    template_name = "create_request.html"

    def dispatch(self, request, *args, **kwargs):
        self.assigned_to = Account.objects.all()
        return super(UpdateRequestView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateRequestView, self).get_form_kwargs()
        kwargs.update({"assigned_to": self.assigned_to})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        case_obj = form.save(commit=False)
        case_obj.save()
        form.save_m2m()
        return redirect("cases:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'case_errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateRequestView, self).get_context_data(**kwargs)
        context["request_obj"] = self.object
        context["case_form"] = context["form"]
        context["request_types"] = RequestTypeChoices.choices
        context["request_priority"] = RequestPriorityChoices.choices
        context["request_status"] = RequestStatusChoices.choices
        return context


class RemoveRequestView(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        request_id = kwargs.get("case_id")
        print(request_id)
        self.object = get_object_or_404(Case, id=request_id)
        self.object.delete()
        return redirect("cases:list")

    def post(self, request, *args, **kwargs):
        request_id = kwargs.get("request_id")
        self.object = get_object_or_404(Case, id=request_id)
        self.object.delete()
        if request.is_ajax():
            return JsonResponse({'error': False})
        count = Case.objects.filter(
            Q(assigned_to=request.user) | Q(created_by=request.user)).distinct().count()
        data = {"request_id": request_id, "count": count}
        return JsonResponse(data)
