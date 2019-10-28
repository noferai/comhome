from django.urls import path
from .views import *


app_name = 'apartments'

urlpatterns = [
	path('', ApartmentListView.as_view(), name='list'),
	path('create/', ApartmentCreateView.as_view(), name='create'),
	path('<int:pk>/view/', ApartmentDetailView.as_view(), name="view"),
	path('<int:pk>/edit/', ApartmentUpdateView.as_view(), name="edit"),
	path('<int:pk>/delete/', ApartmentDeleteView.as_view(), name="remove"),
]
