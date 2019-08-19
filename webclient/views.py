from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, RedirectView, ListView
from django.contrib import messages
from django.urls import reverse
from polls.models import Poll
from news.models import Entry


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "client/index.html"


class NewsListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "client/news/list.html"

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.filter(status=True)
        }
        return {**context, **custom_context}


class PollsListView(LoginRequiredMixin, ListView):
    model = Poll
    template_name = "client/polls/list.html"

    def get_context_data(self, **kwargs):
        context = super(PollsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.filter(status=True)
        }
        return {**context, **custom_context}