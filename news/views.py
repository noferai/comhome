from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, ListView, View, DeleteView)
from django.shortcuts import get_object_or_404, redirect
from .models import Entry
from .forms import EntryForm


class NewsListView(LoginRequiredMixin, TemplateView):
    model = Entry
    template_name = 'news_list.html'

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        custom_context = {
            'news_obj_list': Entry.objects.all(),
        }
        return {**context, **custom_context}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "create_entry.html"

    def dispatch(self, request, *args, **kwargs):
        self.news = Entry.objects.filter(is_published=True).order_by('published_date')
        return super(CreateEntryView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateEntryView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        print(form)
        print(form.is_valid())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        entry_object = form.save(commit=False)
        entry_object.author = self.request.user
        entry_object.save()
        if self.request.POST.get("savenewform"):
            return redirect("news:new_entry")
        else:
            return redirect("news:list")

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_context = {
            'entry_form': context["form"],
            'news_list': self.news,
        }
        return {**context, **custom_context}
#
#
# class EntryDetailView(LoginRequiredMixin, DetailView):
#     model = Entry
#     context_object_name = "entry_record"
#     template_name = "view_entry.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(EntryDetailView, self).get_context_data(**kwargs)
#         entry_record = context["entry_record"]
#         if (
#                 self.request.user in entry_record.assigned_to.all() or
#                 self.request.user == entry_record.created_by
#         ):
#             comment_permission = True
#         else:
#             comment_permission = False
#         context.update({
#             "attachments": entry_record.account_attachment.all(),
#         })
#         return context
#
#
# class EntryUpdateView(LoginRequiredMixin, UpdateView):
#     model = Entry
#     form_class = EntryForm
#     template_name = "create_entry.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         self.news = Entry.objects.filter(is_published=True).order_by('published_date')
#         return super(EntryUpdateView, self).dispatch(request, *args, **kwargs)
#
#     def get_form_kwargs(self):
#         kwargs = super(EntryUpdateView, self).get_form_kwargs()
#         kwargs.update({'assigned_to': self.news})
#         return kwargs
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return self.get_form()
#
#     def form_valid(self, form):
#         # Save Entry
#         entry_object = form.save(commit=False)
#         entry_object.save()
#
#         assigned_to_ids = entry_object.assigned_to.all().values_list('id', flat=True)
#
#         entry_object.assigned_to.clear()
#         entry_object.teams.clear()
#         all_news_list = []
#
#         if self.request.POST.getlist('assigned_to', []):
#             entry_object.assigned_to.add(*self.request.POST.getlist('assigned_to'))
#             assigned_to_list = self.request.POST.getlist('assigned_to')
#             current_site = get_current_site(self.request)
#
#             assigned_form_users = form.cleaned_data.get('assigned_to').values_list('id', flat=True)
#             all_members_list = list(set(list(assigned_form_users)) - set(list(assigned_to_ids)))
#
#             if len(all_members_list):
#                 for assigned_to_user in assigned_to_list:
#                     user = get_object_or_404(Entry, pk=assigned_to_user)
#                     #mail_subject = 'Assigned to account.'
#                     message = render_to_string('assigned_to/account_assigned.html', {
#                         'user': user,
#                         'domain': current_site.domain,
#                         'protocol': self.request.scheme,
#                         'entry': entry_object
#                     })
#                     # email = EmailMessage(mail_subject, message, to=[user.email])
#                     # email.send()
#         if self.request.POST.getlist('teams', []):
#             entry_object.teams.add(*self.request.POST.getlist('teams'))
#         return redirect("accounts:list")
#
#     def form_invalid(self, form):
#         return self.render_to_response(
#             self.get_context_data(form=form)
#         )
#
#     def get_context_data(self, **kwargs):
#         context = super(EntryUpdateView, self).get_context_data(**kwargs)
#         context["account_obj"] = self.object
#         context["account_form"] = context["form"]
#         context["news"] = self.news
#         context["assignedto_list"] = [
#             int(i) for i in self.request.POST.getlist('assigned_to', []) if i]
#         return context
#
#
# class EntryDeleteView(LoginRequiredMixin, DeleteView):
#     model = Entry
#     template_name = 'view_entry.html'
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.delete()
#         return redirect("entry:list")
