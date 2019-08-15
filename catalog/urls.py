from django.urls import path
from .views import *

app_name = 'catalog'

urlpatterns = [
    path('addresses/list/', AddressesListView.as_view(), name='addresses_list'),
    path('addresses/add/', AddressAddView.as_view(), name='address_add'),
    path('addresses/<int:pk>/edit/', AddressEditView.as_view(), name="address_edit"),
    path('addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name="address_remove")
]
