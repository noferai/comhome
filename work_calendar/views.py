from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from .models import Events

# Create your views here.
from schedule.forms import EventForm


@method_decorator(login_required, name='dispatch')
class CalendarPage(TemplateView):
    template_name = 'calendar.html'
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super(CalendarPage, self).get_context_data(**kwargs)
        context['eventlist'] = Events.objects.all()
        return context
