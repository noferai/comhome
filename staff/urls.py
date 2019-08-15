from django.urls import path
from staff.views import (
	StaffListView, CreateStaffView, StaffDetailView, StaffUpdateView,
	StaffDeleteView
)

app_name = 'staff'

urlpatterns = [
	path('list/', StaffListView.as_view(), name='list'),
	path('create/', CreateStaffView.as_view(), name='create'),
	path('<int:pk>/view/', StaffDetailView.as_view(), name="view"),
	path('<int:pk>/edit/', StaffUpdateView.as_view(), name="edit"),
	path('<int:pk>/delete/', StaffDeleteView.as_view(), name="remove"),
]
