from django.urls import path
from news import views

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
]