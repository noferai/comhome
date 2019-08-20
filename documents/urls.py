from django.urls import path
from .views import *

app_name = 'documents'

urlpatterns = [
    path('', DocumentsListView.as_view(), name='list'),
    path('create/', DocumentAddView.as_view(), name='create'),
    path('<int:pk>/edit/', DocumentEditView.as_view(), name="edit"),
    path('<int:pk>/delete/', DocumentDeleteView.as_view(), name="remove"),
]
