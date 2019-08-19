from django.urls import path
from .views import PollsListView, PollCreateView, PollDetailView, PollResultsView, vote

app_name = 'polls'

urlpatterns = [
    path('', PollsListView.as_view(), name='list'),
    path('create/', PollCreateView.as_view(), name='create'),
    path('<int:pk>/', PollDetailView.as_view(), name='detail'),
    path('<int:pk>/results/', PollResultsView.as_view(), name='results'),
    path('<int:pk>/vote/', vote, name='vote')
]
