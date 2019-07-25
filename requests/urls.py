from django.urls import path
from requests.views import *

app_name = 'requests'

urlpatterns = [
    path('list/', RequestsListView.as_view(), name='list'),
    path('create/', CreateRequestView.as_view(), name='add'),
    path('<int:pk>/view/', RequestDetailView.as_view(), name="view"),
    path('<int:pk>/edit_request/', UpdateRequestView.as_view(), name="edit"),
    path('<int:pk>/remove/', RemoveRequestView.as_view(), name="remove"),
    #TODO: Закрытие заявки, быстрая смена статуса. Комментарии и вложения(в т.ч. документы)
]
