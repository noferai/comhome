from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View)
from apartments.models import Apartment
from common.models import Comment, Attachments
from homeowners.models import Homeowner
from homeowners.forms import HomeownerCommentForm, HomeownerForm, HomeownerAttachmentForm


class HomeownerListView(LoginRequiredMixin, TemplateView):
    model = Homeowner
    context_object_name = "objects"
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super(HomeownerListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'per_page': self.request.POST.get('per_page'),
            'fields': ['created_on', 'name', 'debt', 'apartments'],
            'urls': {
                'add': 'homeowners:add',
                'detail': 'homeowners:view',
                'edit': 'homeowners:edit',
                'remove': 'homeowners:remove',
                'apartments': 'apartments:view'
            }
        }
        return {**context, **custom_context}

    def post(self, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateHomeownerView(LoginRequiredMixin, CreateView):
    model = Homeowner
    form_class = HomeownerForm
    template_name = "homeowners/create.html"

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
        homeowner_obj = form.save(commit=False)
        homeowner_obj.created_by = self.request.user
        homeowner_obj.save()
        if self.apartments.count() > 0:
            form.save_m2m()
        if self.request.POST.get("savenewform"):
            return redirect("homeowners:add")
        else:
            return redirect('homeowners:list')

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateHomeownerView, self).get_context_data(**kwargs)
        context["homeowner_form"] = context["form"]
        return context


class HomeownerDetailView(LoginRequiredMixin, DetailView):
    model = Homeowner
    context_object_name = "homeowner"
    template_name = "homeowners/detail.html"

    def get_context_data(self, **kwargs):
        context = super(HomeownerDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(homeowner__id=self.object.id).order_by('-id')
        attachments = Attachments.objects.filter(homeowner__id=self.object.id).order_by('-id')
        context.update({
            "attachments": attachments, "comments": comments})
        return context


class UpdateHomeownerView(LoginRequiredMixin, UpdateView):
    model = Homeowner
    form_class = HomeownerForm
    template_name = "homeowners/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.error = "" # Зачем?
        self.apartments = Apartment.objects.all()
        return super(UpdateHomeownerView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(UpdateHomeownerView, self).get_initial()
        status = self.request.GET.get('status', None)
        if status:
            initial.update({"status": status})
        return initial

    def get_form_kwargs(self):
        kwargs = super(UpdateHomeownerView, self).get_form_kwargs()
        kwargs.update({"apartments": self.apartments})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateHomeownerView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        homeowner_obj = form.save(commit=False)
        homeowner_obj.save()
        form.save_m2m()
        return redirect('homeowners:list')

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateHomeownerView, self).get_context_data(**kwargs)
        context["homeowner_obj"] = self.object
        context["homeowner_form"] = context["form"]
        context["error"] = self.error
        return context


class DeleteHomeownerView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(**kwargs)

    def post(self, **kwargs):
        self.object = get_object_or_404(Homeowner, id=kwargs.get("pk"))
        self.object.delete()
        return redirect("homeowners:list")


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = HomeownerCommentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.homeowner = get_object_or_404(Homeowner, id=request.POST.get('leadid'))
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commented_by = self.request.user
        comment.homeowner = self.homeowner
        comment.save()
        return JsonResponse({
            "comment_id": comment.id, "comment": comment.comment,
            "commented_on": comment.commented_on,
            "commented_by": comment.commented_by.email
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['comment'].errors})


class UpdateCommentView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request):
        self.comment_obj = get_object_or_404(Comment, id=request.POST.get("commentid"))
        if request.user == self.comment_obj.commented_by:
            form = HomeownerCommentForm(request.POST, instance=self.comment_obj)
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
            "commentid": self.comment_obj.id,
            "comment": self.comment_obj.comment,
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['comment'].errors})


class DeleteCommentView(LoginRequiredMixin, View):

    def post(self, request):
        self.object = get_object_or_404(Comment, id=request.POST.get("comment_id"))
        self.object.delete()
        data = {"cid": request.POST.get("comment_id")}
        return JsonResponse(data)


class AddAttachmentsView(LoginRequiredMixin, CreateView):
    model = Attachments
    form_class = HomeownerAttachmentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.homeowner = get_object_or_404(Homeowner, id=request.POST.get('Homeownerid'))
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        attachment = form.save(commit=False)
        attachment.created_by = self.request.user
        attachment.file_name = attachment.attachment.name
        attachment.homeowner = self.homeowner
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

    def post(self, request):
        self.object = get_object_or_404(Attachments, id=request.POST.get("attachment_id"))
        self.object.delete()
        data = {"aid": request.POST.get("attachment_id")}
        return JsonResponse(data)
