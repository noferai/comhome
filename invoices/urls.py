from django.urls import path
from .views import *

app_name = 'invoices'

urlpatterns = [
    # path('<int:pk>/view/', InvoiceDetailView.as_view(), name="view"),
    path('', InvoiceListView.as_view(), name='list'),
    path('create/', InvoiceAddView.as_view(), name='create'),
    path('<int:pk>/edit/', InvoiceEditView.as_view(), name="edit"),
    path('<int:pk>/delete/', InvoiceDeleteView.as_view(), name="remove"),
]
