from django.urls import path
from staff.views import (
	StaffListView, CreateStaffView, StaffDetailView, StaffUpdateView,
	StaffDeleteView, AddCommentView, UpdateCommentView, DeleteCommentView,
	AddAttachmentView, DeleteAttachmentsView
)

app_name = 'staff'

urlpatterns = [
	path('list/', StaffListView.as_view(), name='list'),
	path('create/', CreateStaffView.as_view(), name='add'),
	path('<int:pk>/view/', StaffDetailView.as_view(), name="view"),
	path('<int:pk>/edit/', StaffUpdateView.as_view(), name="edit"),
	path('<int:pk>/delete/', StaffDeleteView.as_view(), name="remove"),
	path('comment/add/', AddCommentView.as_view(), name="add_comment"),
	path('comment/edit/', UpdateCommentView.as_view(), name="edit_comment"),
	path('comment/remove/', DeleteCommentView.as_view(), name="remove_comment"),

	path('attachment/add/', AddAttachmentView.as_view(), name="add_attachment"),
	path('attachment/remove/', DeleteAttachmentsView.as_view(), name="remove_attachment"),
]
