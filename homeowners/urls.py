from django.urls import path
from homeowners.views import (
    HomeownerListView, CreateHomeownerView, HomeownerDetailView, UpdateHomeownerView, DeleteHomeownerView,
    AddCommentView, UpdateCommentView, DeleteCommentView, AddAttachmentsView, DeleteAttachmentsView)

app_name = 'homeowners'


urlpatterns = [
    path('list/', HomeownerListView.as_view(), name='list'),
    path('create/', CreateHomeownerView.as_view(), name='add'),
    path('<int:pk>/view/', HomeownerDetailView.as_view(), name="view"),
    path('<int:pk>/edit/', UpdateHomeownerView.as_view(), name="edit"),
    path('<int:pk>/delete/', DeleteHomeownerView.as_view(), name="remove"),

    path('comment/add/', AddCommentView.as_view(), name="add_comment"),
    path('comment/edit/', UpdateCommentView.as_view(), name="edit_comment"),
    path('comment/remove/', DeleteCommentView.as_view(), name="remove_comment"),

    path('attachment/add/', AddAttachmentsView.as_view(), name="add_attachment"),
    path('attachment/remove/', DeleteAttachmentsView.as_view(), name="remove_attachment"),
]
