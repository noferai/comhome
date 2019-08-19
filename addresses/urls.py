from django.urls import path
from .views import *

app_name = 'addresses'

urlpatterns = [
    path('', AddressesListView.as_view(), name='list'),
    path('create/', AddressAddView.as_view(), name='create'),
    path('<int:pk>/edit/', AddressEditView.as_view(), name="edit"),
    path('<int:pk>/delete/', AddressDeleteView.as_view(), name="remove")
]
