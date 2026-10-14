from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView

from .views import (
    CurrentUserView, LoginView, RegistrationView,
    PasswordChangeView,
    StaffListCreateView, StaffDetailView, StaffActivateView
)

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),

    # Staff management (admin only)
    path('', StaffListCreateView.as_view(), name='staff-list-create'),
    path('<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    path('<int:pk>/activate/', StaffActivateView.as_view(), name='staff-activate'),
]