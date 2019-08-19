from django.urls import path
from .views import HomeView, NewsListView, PollsListView, PollDetailView, PollResultsView, vote

app_name = 'client'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news/', NewsListView.as_view(), name='news'),
    path('polls/', PollsListView.as_view(), name='polls'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/<int:pk>/results/', PollResultsView.as_view(), name='poll-results'),
    path('polls/<int:pk>/vote/', vote, name='poll-vote')
]
