from django.urls import path
from .views import PollsListView, PollCreateView

app_name = 'polls'

urlpatterns = [
    path('', PollsListView.as_view(), name='list'),
    path('create/', PollCreateView.as_view(), name='create')
]
