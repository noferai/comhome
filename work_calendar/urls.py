from django.urls import path

from work_calendar.views import CalendarView

app_name = 'work_calendar'

urlpatterns = [
    path('test/', CalendarView.as_view())
]