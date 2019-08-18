from django.contrib.auth import views as auth_views
from django.urls import path
from ComfortableHome.views import *
from users.views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'users'


urlpatterns = [
    path('', CRMHomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    # path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Admin views
    path('users/list/', AdminsListView.as_view(), name='list'),
    path('users/create/', CreateAdminView.as_view(), name='create'),
    path('users/<int:pk>/edit/', UpdateAdminView.as_view(), name="edit"),
    path('users/<int:pk>/view/', AdminDetailView.as_view(), name='view'),
    path('users/<int:pk>/delete/', AdminDeleteView.as_view(), name='remove'),

    path(
        'password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # api
    # path('api/', include('api.urls', namespace='api')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
