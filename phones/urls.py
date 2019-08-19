from django.urls import path
from .views import *

app_name = 'phones'

urlpatterns = [
    path('', PhonesListView.as_view(), name='list'),
    path('create/', PhoneAddView.as_view(), name='create'),
    path('<int:pk>/edit/', PhoneEditView.as_view(), name="edit"),
    path('<int:pk>/delete/', PhoneDeleteView.as_view(), name="remove")
]
