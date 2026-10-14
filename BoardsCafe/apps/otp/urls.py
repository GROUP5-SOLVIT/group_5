from django.urls import path
from .views import OTPRequestView, OTPVerifyView

app_name = 'otp'

urlpatterns = [
    path('request/', OTPRequestView.as_view(), name='otp-request'),
    path('verify/', OTPVerifyView.as_view(), name='otp-verify'),
]