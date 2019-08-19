from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from .models import Events


@method_decorator(login_required, name='dispatch')
class CalendarPage(TemplateView):
    template_name = 'work_calendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarPage, self).get_context_data(**kwargs)
        context['eventlist'] = Events.objects.all()
        return context
