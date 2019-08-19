from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse
from polls.models import Poll, Choice
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


class PollDetailView(DetailView):
    model = Poll
    template_name = 'client/polls/detail.html'


class PollResultsView(DetailView):
    model = Poll
    template_name = 'client/polls/results.html'


def vote(request, pk):
    p = get_object_or_404(Poll, pk=pk)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'client/polls/detail.html', {
            'poll': p,
            'error_message': "Вы не сделали выбор.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('client:poll-results', args=(p.id,)))
