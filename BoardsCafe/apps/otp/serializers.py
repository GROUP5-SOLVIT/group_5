from rest_framework import serializers
from django.conf import settings


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpose = serializers.ChoiceField(choices=[
        ('EMAIL_VERIFICATION', 'Email Verification'),
        ('PASSWORD_RESET', 'Password Reset'),
        ('ACCOUNT_VERIFICATION', 'Account Verification'),
        ('LOGIN_2FA', 'Two-Factor Authentication'),
    ])


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=4, max_length=10)
    purpose = serializers.ChoiceField(choices=[
        ('EMAIL_VERIFICATION', 'Email Verification'),
        ('PASSWORD_RESET', 'Password Reset'),
        ('ACCOUNT_VERIFICATION', 'Account Verification'),
        ('LOGIN_2FA', 'Two-Factor Authentication'),
    ])


class OTPResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = serializers.DictField(required=False)
    errors = serializers.DictField(required=False)