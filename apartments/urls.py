from django.urls import path
from .views import *


app_name = 'apartments'

urlpatterns = [
	path('list/', ApartmentListView.as_view(), name='list'),
	path('add/', ApartmentAddView.as_view(), name='add'),
	path('<int:pk>/view/', ApartmentDetailView.as_view(), name="detail"),
	path('<int:pk>/edit/', ApartmentEditView.as_view(), name="edit"),
	path('<int:pk>/delete/', ApartmentDeleteView.as_view(), name="remove"),
	path('comment/add/', AddCommentView.as_view(), name="add_comment"),
	path('comment/edit/', EditCommentView.as_view(), name="edit_comment"),
	path('comment/remove/', DeleteCommentView.as_view(), name="remove_comment"),

	path('attachment/add/', AddAttachmentView.as_view(), name="add_attachment"),
	path('attachment/remove/', DeleteAttachmentsView.as_view(), name="remove_attachment"),
]
