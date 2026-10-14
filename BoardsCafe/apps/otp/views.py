from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import OTPRequestSerializer, OTPVerifySerializer
from .services import OTPService
from .throttling import OTPRateThrottle
from BoardsCafe.core.responses import success_response, error_response

User = get_user_model()


class OTPRequestView(generics.CreateAPIView):
    serializer_class = OTPRequestSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email'].strip().lower()
        purpose = serializer.validated_data['purpose']

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return success_response(
                message='If the email exists, an OTP has been sent.'
            )

        if not OTPService.can_resend_otp(user, purpose):
            from django.conf import settings
            cooldown = getattr(settings, 'OTP_RESEND_COOLDOWN_SECONDS', 60)
            return error_response(
                message=f'Please wait {cooldown} seconds before requesting another OTP.',
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )

        otp, otp_code = OTPService.create_otp(user, purpose)
        OTPService.send_otp_email(user, otp_code, purpose)
        OTPService.record_otp_sent(user, purpose)

        return success_response(
            message='If the email exists, an OTP has been sent.'
        )


class OTPVerifyView(generics.CreateAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email'].strip().lower()
        otp_code = serializer.validated_data['otp']
        purpose = serializer.validated_data['purpose']

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return error_response(
                message='Invalid OTP.',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        is_valid, message = OTPService.verify_otp(user, otp_code, purpose)

        if not is_valid:
            return error_response(
                message=message,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return success_response(
            data={'verified': True},
            message=message
        )