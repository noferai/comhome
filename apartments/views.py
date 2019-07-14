from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from apartments.forms import ApartmentForm, ApartmentCommentForm, ApartmentAttachmentForm
from apartments.models import Apartment
from homeowners.models import Homeowner
from catalog.models import Address
from common.models import Comment, Attachments
from common.utils import ApartmentStatusChoices


class ApartmentListView(LoginRequiredMixin, TemplateView):
    model = Apartment
    context_object_name = "apartments_list"
    template_name = "apartments/list.html"

    def dispatch(self, request, *args, **kwargs):
        self.owners = Homeowner.objects.all()
        return super(ApartmentListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ApartmentListView, self).get_context_data(**kwargs)
        context["owners"] = self.owners
        context["apartments_list"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ApartmentAddView(LoginRequiredMixin, CreateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = "apartments/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.addresses = Address.objects.all()
        return super(ApartmentAddView, self).dispatch(request, *args, **kwargs)

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
        account_object = form.save(commit=False)
        account_object.created_by = self.request.user
        account_object.save()
        if self.request.POST.get("savenewform"):
            return redirect("apartments:add")
        else:
            return redirect("apartments:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ApartmentAddView, self).get_context_data(**kwargs)
        context["apartment_form"] = context["form"]
        context["apartment_status"] = ApartmentStatusChoices.choices
        return context


class ApartmentDetailView(LoginRequiredMixin, DetailView):
    model = Apartment
    context_object_name = "apartment"
    template_name = "apartments/detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.addresses = Address.objects.all()
        return super(ApartmentDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApartmentDetailView, self).get_context_data(**kwargs)
        return context


class ApartmentEditView(LoginRequiredMixin, UpdateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = "apartments/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.addresses = Address.objects.all()
        return super(ApartmentEditView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ApartmentEditView, self).get_form_kwargs()
        kwargs.update({"addresses": self.addresses})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        apartment_object = form.save(commit=False)
        apartment_object.save()
        return redirect("apartments:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(ApartmentEditView, self).get_context_data(**kwargs)
        context["apartment_obj"] = self.object
        context["apartment_form"] = context["form"]
        return context


class ApartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Apartment
    template_name = 'apartments/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("apartments:list")


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = ApartmentCommentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.account = get_object_or_404(Apartment, id=request.POST.get('accountid'))
        data = {'error': "You don't have permission to comment for this account."}
        return JsonResponse(data)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commented_by = self.request.user
        comment.account = self.account
        comment.save()
        return JsonResponse({
            "comment_id": comment.id, "comment": comment.comment,
            "commented_on": comment.commented_on,
            "commented_by": comment.commented_by.email
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['comment'].errors})


class EditCommentView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.comment_obj = get_object_or_404(Comment, id=request.POST.get("commentid"))
        if request.user == self.comment_obj.commented_by:
            form = ApartmentCommentForm(request.POST, instance=self.comment_obj)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            data = {'error': "You don't have permission to edit this comment."}
            return JsonResponse(data)

    def form_valid(self, form):
        self.comment_obj.comment = form.cleaned_data.get("comment")
        self.comment_obj.save(update_fields=["comment"])
        return JsonResponse({
            "comment_id": self.comment_obj.id,
            "comment": self.comment_obj.comment,
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['comment'].errors})


class DeleteCommentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(Comment, id=request.POST.get("comment_id"))
        self.object.delete()
        data = {"cid": request.POST.get("comment_id")}
        return JsonResponse(data)


class AddAttachmentView(LoginRequiredMixin, CreateView):
    model = Attachments
    form_class = ApartmentAttachmentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.account = get_object_or_404(Apartment, id=request.POST.get('accountid'))
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        attachment = form.save(commit=False)
        attachment.created_by = self.request.user
        attachment.file_name = attachment.attachment.name
        attachment.account = self.account
        attachment.save()
        return JsonResponse({
            "attachment_id": attachment.id,
            "attachment": attachment.file_name,
            "attachment_url": attachment.attachment.url,
            "created_on": attachment.created_on,
            "created_by": attachment.created_by.email
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['attachment'].errors})


class DeleteAttachmentsView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(Attachments, id=request.POST.get("attachment_id"))
        if request.user == self.object.created_by:
            self.object.delete()
            data = {"acd": request.POST.get("attachment_id")}
            return JsonResponse(data)
        else:
            data = {'error': "You don't have permission to delete this attachment."}
            return JsonResponse(data)
