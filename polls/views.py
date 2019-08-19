from django.urls import reverse
from django.db import transaction
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django.views.generic import CreateView, DetailView
from ComfortableHome.mixins import AdminRequiredMixin
from .models import Choice, Poll
from .tables import PollsTable, PollFilter
from .forms import PollForm, ChoiceFormSet


class PollsListView(AdminRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Poll
    table_class = PollsTable
    template_name = "crm/list.html"
    export_name = "Oprosy"
    filterset_class = PollFilter

    def get_context_data(self, **kwargs):
        context = super(PollsListView, self).get_context_data(**kwargs)
        custom_context = {
            'objects': self.model.objects.all(),
            'urls': {
                'add': 'polls:create',
            }
        }
        return {**context, **custom_context}


class PollCreateView(CreateView):
    model = Poll
    form_class = PollForm
    template_name = "crm/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['formset'] = ChoiceFormSet()
        custom_context = {
            'formset_prefix': 'choice_set',
            'formset_title': 'Варианты ответов',
            'urls': {
                'list': 'polls:list',
            }
        }
        return {**context, **custom_context}

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context['formset']
        with transaction.atomic():
            self.object = form.save()

            if choices.is_valid():
                choices.instance = self.object
                choices.save()
        if self.request.POST.get("save_new"):
            return redirect("polls:create")
        else:
            return redirect("polls:list")


class PollDetailView(DetailView):
    model = Poll
    template_name = 'client/polls/detail.html'


class PollResultsView(DetailView):
    model = Poll
    template_name = 'client/polls/results.html'


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'client/polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
