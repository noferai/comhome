from django.urls import path
from .views import HomeView, NewsListView, PollsListView

app_name = 'client'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news/', NewsListView.as_view(), name='news'),
    path('polls/', PollsListView.as_view(), name='polls'),
]
