from django.urls import path
from clients.views import (
    ClientListView, CreateClientView, ClientDetailView, UpdateClientView, DeleteClientView)

app_name = 'clients'


urlpatterns = [
    path('', ClientListView.as_view(), name='list'),
    path('create/', CreateClientView.as_view(), name='create'),
    path('<int:pk>/view/', ClientDetailView.as_view(), name="view"),
    path('<int:pk>/edit/', UpdateClientView.as_view(), name="edit"),
    path('<int:pk>/delete/', DeleteClientView.as_view(), name="remove")
]
