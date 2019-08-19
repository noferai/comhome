from django.conf import settings
from django.contrib.auth import views
from django.urls import include, path
from .views import handler404, handler500

app_name = 'ComfortableHome'

urlpatterns = [
    path('', include('users.urls', namespace="users")),
    path('', include('django.contrib.auth.urls')),
    path('client/', include('webclient.urls', namespace="client")),
    path('staff/', include('staff.urls', namespace="staff")),
    path('apartments/', include('apartments.urls', namespace="apartments")),
    path('homeowners/', include('homeowners.urls', namespace="homeowners")),
    path('polls/', include('polls.urls', namespace="polls")),
    path('requests/', include('requests.urls', namespace="requests")),
    path('addresses/', include('addresses.urls', namespace="addresses")),
    path('phones/', include('phones.urls', namespace="phones")),
    path('invoices/', include('invoices.urls', namespace="invoices")),
    path('news/', include('news.urls', namespace='news')),
    path('logout/', views.LogoutView, {'next_page': '/login/'}, name="logout"),
    path('comment/', include('comment.urls')),
    path('calendar/', include('work_calendar.urls', namespace='work_calendar'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = handler404
handler500 = handler500
