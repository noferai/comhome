from django.urls import path
from homeowners.views import (
    HomeownerListView, CreateHomeownerView, HomeownerDetailView, UpdateHomeownerView, DeleteHomeownerView)

app_name = 'homeowners'


urlpatterns = [
    path('', HomeownerListView.as_view(), name='list'),
    path('create/', CreateHomeownerView.as_view(), name='create'),
    path('<int:pk>/view/', HomeownerDetailView.as_view(), name="view"),
    path('<int:pk>/edit/', UpdateHomeownerView.as_view(), name="edit"),
    path('<int:pk>/delete/', DeleteHomeownerView.as_view(), name="remove")
]
