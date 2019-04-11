from django.urls import path, re_path
from news.views import *

app_name = 'news'

urlpatterns = [
    path('', news_list, name='news_list'),
]
