from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, DeleteView

from rest_framework.views import APIView
from rest_framework.response import Response

from requests.models import Request
from requests.forms import RequestForm
from staff.models import Staff

from common.utils import RequestTypeChoices, RequestPriorityChoices, RequestStatusChoices


class RequestsListView(LoginRequiredMixin, TemplateView):
    model = Request
    context_object_name = "requests"
    template_name = "requests.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
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
    model = Request
    form_class = RequestForm
    template_name = "create_request.html"

    def dispatch(self, request, *args, **kwargs):
        self.assigned_to = Staff.objects.all()
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
        request = form.save(commit=False)
        request.created_by = self.request.user
        request.save()
        form.save_m2m()
        if self.request.POST.get("savenewform"):
            return redirect("requests:create")
        else:
            return redirect("requests:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateRequestView, self).get_context_data(**kwargs)
        context["request_form"] = context["form"]
        context["request_types"] = RequestTypeChoices.choices
        context["request_priority"] = RequestPriorityChoices.choices
        context["request_status"] = RequestStatusChoices.choices
        return context


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    context_object_name = "request_record"
    template_name = "view_request.html"

    def dispatch(self, request, *args, **kwargs):
        self.assigned_to = Request.objects.all()
        return super(RequestDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequestDetailView, self).get_context_data(**kwargs)
        return context


class UpdateRequestView(LoginRequiredMixin, UpdateView):
    model = Request
    form_class = RequestForm
    template_name = "create_request.html"

    def dispatch(self, request, *args, **kwargs):
        self.assigned_to = Staff.objects.all()
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
        request_obj = form.save(commit=False)
        request_obj.save()
        form.save_m2m()
        return redirect("requests:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'request_errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateRequestView, self).get_context_data(**kwargs)
        context["request_obj"] = self.object
        context["request_form"] = context["form"]
        context["request_types"] = RequestTypeChoices.choices
        context["request_priority"] = RequestPriorityChoices.choices
        context["request_status"] = RequestStatusChoices.choices
        return context


class RemoveRequestView(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        return self.post(**kwargs)

    def post(self, **kwargs):
        self.object = get_object_or_404(Request, id=kwargs.get("pk"))
        self.object.delete()
        return redirect("requests:list")
