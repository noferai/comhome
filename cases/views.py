from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView, View, DeleteView

from rest_framework.views import APIView
from rest_framework.response import Response

from cases.models import Case
from cases.forms import CaseForm, CaseCommentForm, CaseAttachmentForm
from common.models import Team, User, Comment, Attachments
from accounts.models import Account
from contacts.models import Contact
from common.utils import RequestTypeChoices, RequestPriorityChoices, RequestStatusChoices, CASE_TYPE, PRIORITY_CHOICE, \
    STATUS_CHOICE
import json


class RequestsListView(LoginRequiredMixin, TemplateView):
    model = Case
    context_object_name = "requests"
    template_name = "requests.html"

    def get_queryset(self):
        queryset = self.model.objects.all()  # Хуйня какая-то блядская
        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(name__icontains=request_post.get('name'))
            if request_post.get('account'):
                queryset = queryset.filter(account_id=request_post.get('account'))
            if request_post.get('status'):
                queryset = queryset.filter(status=request_post.get('status'))
            if request_post.get('priority'):
                queryset = queryset.filter(priority=request_post.get('priority'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RequestsListView, self).get_context_data(**kwargs)
        context["requests"] = self.get_queryset()
        context["staff"] = Account.objects.all()
        context["per_page"] = self.request.POST.get('per_page')
        context["acc"] = int(self.request.POST.get("account")) if self.request.POST.get("account") else None
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
        self.staff = Account.objects.all()
        return super(CreateRequestView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateRequestView, self).get_form_kwargs()
        kwargs.update({"assigned_to": self.staff})
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
        # if self.request.POST.getlist('assigned_to', []):
        #     case.assigned_to.add(*self.request.POST.getlist('assigned_to'))
        #     assigned_to_list = self.request.POST.getlist('assigned_to')
        #     current_site = get_current_site(self.request)
        #     for assigned_to_user in assigned_to_list:
        #         user = get_object_or_404(User, pk=assigned_to_user)
        #         mail_subject = 'Assigned to case.'
        #         message = render_to_string('assigned_to/cases_assigned.html', {
        #             'user': user,
        #             'domain': current_site.domain,
        #             'protocol': self.request.scheme,
        #             'case': case
        #         })
        #         email = EmailMessage(mail_subject, message, to=[user.email])
        #         email.send()
        if self.request.is_ajax():
            return JsonResponse({'error': False})
        return redirect('cases:list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'case_errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CreateRequestView, self).get_context_data(**kwargs)
        context["teams"] = Team.objects.all()
        context["case_form"] = context["form"]
        context["staff"] = self.staff
        context["request_types"] = RequestTypeChoices.choices
        context["request_priority"] = RequestPriorityChoices.choices
        context["request_status"] = RequestStatusChoices.choices
        context["assignedto_list"] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i]
        context["teams_list"] = [
            int(i) for i in self.request.POST.getlist('teams', []) if i]
        context["contacts_list"] = [
            int(i) for i in self.request.POST.getlist('contacts', []) if i]
        return context

class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Case
    context_object_name = "request_record"
    template_name = "view_request.html"

    def get_queryset(self):
        queryset = super(RequestDetailView, self).get_queryset()
        return queryset.prefetch_related("assigned_to")

    # def get_context_data(self, **kwargs):
    #     context = super(RequestDetailView, self).get_context_data(**kwargs)
    #     context.update({"comments": context["case_record"].cases.all(),
    #         "attachments": context['case_record'].case_attachment.all()})
    #     return context


class UpdateRequestView(LoginRequiredMixin, UpdateView):
    model = Case
    form_class = CaseForm
    template_name = "create_request.html"

    def dispatch(self, request, *args, **kwargs):
        #self.users = User.objects.filter(is_active=True).order_by('email')
        self.staff = Account.objects.all()
        return super(UpdateRequestView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateRequestView, self).get_form_kwargs()
        kwargs.update({"assigned_to": self.staff})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        case_obj = form.save()

        assigned_to_ids = case_obj.assigned_to.all().values_list('id', flat=True)
        case_obj.assigned_to.clear()
        #case_obj.teams.clear()
        #case_obj.contacts.clear()
        # if self.request.POST.getlist('assigned_to', []):
        #     case_obj.assigned_to.add(*self.request.POST.getlist('assigned_to'))
        #     assigned_to_list = self.request.POST.getlist('assigned_to')
        #     current_site = get_current_site(self.request)
        #     assigned_form_users = form.cleaned_data.get('assigned_to').values_list('id', flat=True)
        #     all_members_list = list(set(list(assigned_form_users)) - set(list(assigned_to_ids)))
        #     if len(all_members_list):
        #         for assigned_to_user in assigned_to_list:
        #             user = get_object_or_404(User, pk=assigned_to_user)
        #             mail_subject = 'Assigned to case.'
        #             message = render_to_string('assigned_to/cases_assigned.html', {
        #                 'user': user,
        #                 'domain': current_site.domain,
        #                 'protocol': self.request.scheme,
        #                 'case': case_obj
        #             })
        #             email = EmailMessage(mail_subject, message, to=[user.email])
        #             email.send()

        if self.request.POST.getlist('teams', []):
            case_obj.teams.add(*self.request.POST.getlist('teams'))
        if self.request.POST.getlist('contacts', []):
            case_obj.contacts.add(*self.request.POST.getlist('contacts'))
        if self.request.is_ajax():
            return JsonResponse({'error': False})
        return redirect("cases:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'case_errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UpdateRequestView, self).get_context_data(**kwargs)
        #context["teams"] = Team.objects.all()
        context["case_form"] = context["form"]
        context["staff"] = self.staff
        context["request_types"] = RequestTypeChoices.choices
        context["request_priority"] = RequestPriorityChoices.choices
        context["request_status"] = RequestStatusChoices.choices
        context["assignedto_list"] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i]
        context["teams_list"] = [
            int(i) for i in self.request.POST.getlist('teams', []) if i]
        context["contacts_list"] = [
            int(i) for i in self.request.POST.getlist('contacts', []) if i]
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

# class CloseCaseView(LoginRequiredMixin, View):
#
#     def post(self, request, *args, **kwargs):
#         case_id = request.POST.get("case_id")
#         self.object = get_object_or_404(Case, id=case_id)
#         self.object.status = "Closed"
#         self.object.save()
#         data = {'status': "Closed", "cid": case_id}
#         return JsonResponse(data)


# class SelectContactsView(LoginRequiredMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         contact_account = request.GET.get("account")
#         if contact_account:
#             account = get_object_or_404(Account, id=contact_account)
#             contacts = Contact.objects.filter(account=account)
#         else:
#             contacts = Contact.objects.all()
#         data = {i.pk: i.first_name for i in contacts.distinct()}
#         return JsonResponse(data)


# class GetRequestsView(LoginRequiredMixin, ListView):
#     model = Request
#     context_object_name = "requests"
#     template_name = "cases_list.html"


# class AddCommentView(LoginRequiredMixin, CreateView):
#     model = Comment
#     form_class = CaseCommentForm
#     http_method_names = ["post"]
#
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         self.case = get_object_or_404(Case, id=request.POST.get('caseid'))
#         if (
#             request.user in self.case.assigned_to.all() or
#             request.user == self.case.created_by
#         ):
#             form = self.get_form()
#             if form.is_valid():
#                 return self.form_valid(form)
#             else:
#                 return self.form_invalid(form)
#         else:
#             data = {'error': "You don't have permission to comment."}
#             return JsonResponse(data)
#
#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.commented_by = self.request.user
#         comment.case = self.case
#         comment.save()
#         return JsonResponse({
#             "comment_id": comment.id, "comment": comment.comment,
#             "commented_on": comment.commented_on,
#             "commented_by": comment.commented_by.email
#         })
#
#     def form_invalid(self, form):
#         return JsonResponse({"error": form['comment'].errors})


# class UpdateCommentView(LoginRequiredMixin, View):
#     http_method_names = ["post"]
#
#     def post(self, request, *args, **kwargs):
#         self.comment_obj = get_object_or_404(Comment, id=request.POST.get("commentid"))
#         if request.user == self.comment_obj.commented_by:
#             form = CaseCommentForm(request.POST, instance=self.comment_obj)
#             if form.is_valid():
#                 return self.form_valid(form)
#             else:
#                 return self.form_invalid(form)
#         else:
#             data = {'error': "You don't have permission to edit this comment."}
#             return JsonResponse(data)
#
#     def form_valid(self, form):
#         self.comment_obj.comment = form.cleaned_data.get("comment")
#         self.comment_obj.save(update_fields=["comment"])
#         return JsonResponse({
#             "comment_id": self.comment_obj.id,
#             "comment": self.comment_obj.comment,
#         })
#
#     def form_invalid(self, form):
#         return JsonResponse({"error": form['comment'].errors})


# class DeleteCommentView(LoginRequiredMixin, View):
#
#     def post(self, request, *args, **kwargs):
#         self.object = get_object_or_404(Comment, id=request.POST.get("comment_id"))
#         if request.user == self.object.commented_by:
#             self.object.delete()
#             data = {"cid": request.POST.get("comment_id")}
#             return JsonResponse(data)
#         else:
#             data = {'error': "You don't have permission to delete this comment."}
#             return JsonResponse(data)


# class AddAttachmentView(LoginRequiredMixin, CreateView):
#     model = Attachments
#     form_class = CaseAttachmentForm
#     http_method_names = ["post"]
#
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         self.case = get_object_or_404(Case, id=request.POST.get('caseid'))
#         if (
#             request.user in self.case.assigned_to.all() or
#             request.user == self.case.created_by
#         ):
#             form = self.get_form()
#             if form.is_valid():
#                 return self.form_valid(form)
#             else:
#                 return self.form_invalid(form)
#         else:
#             data = {'error': "You don't have permission to add attachment for this case."}
#             return JsonResponse(data)
#
#     def form_valid(self, form):
#         attachment = form.save(commit=False)
#         attachment.created_by = self.request.user
#         attachment.file_name = attachment.attachment.name
#         attachment.case = self.case
#         attachment.save()
#         return JsonResponse({
#               "message": "Attachment Saved"
#         })
#
#     def form_invalid(self, form):
#         return JsonResponse({"error": form['attachment'].errors})


# class DeleteAttachmentsView(LoginRequiredMixin, View):
#
#     def post(self, request, *args, **kwargs):
#         self.object = get_object_or_404(Attachments, id=request.POST.get("attachment_id"))
#         if request.user == self.object.created_by:
#             self.object.delete()
#             data = {"acd": request.POST.get("attachment_id")}
#             return JsonResponse(data)
#         else:
#             data = {'error': "You don't have permission to delete this attachment."}
#             return JsonResponse(data)


class SendFormsApi(APIView):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        user_id = data['user_id']
        type = data['type']
        description = data['description']

        case = Case()

        if type == 'electrician':
            case.request_type = RequestTypeChoices.electrical
        elif type == 'plumber':
            case.request_type = RequestTypeChoices.plumb
        elif type == 'cleaner':
            case.request_type = RequestTypeChoices.cleaner
        else:
            case.request_type = RequestTypeChoices.other

        case.description = description
        case.created_by = User.objects.get(id=user_id)
        case.save()

        return Response({'isSuccess': True})

