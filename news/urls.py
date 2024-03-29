from django.urls import path
from news.views import *

app_name = 'news'

urlpatterns = [
    path('', NewsListView.as_view(), name='list'),
    path('create/', CreateEntryView.as_view(), name='create'),
    path('<int:pk>/view/', EntryDetailView.as_view(), name="view"),
    path('<int:pk>/edit/', EntryUpdateView.as_view(), name="edit"),
    path('<int:pk>/delete/', EntryDeleteView.as_view(), name="remove"),
]
