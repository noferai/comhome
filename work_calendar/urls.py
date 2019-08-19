from django.urls import path

from work_calendar.views import CalendarPage

app_name = 'work_calendar'

urlpatterns = [
    path('test/', CalendarPage.as_view())
]