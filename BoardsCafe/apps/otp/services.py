from django.conf import settings
from django.utils import timezone

from .models import OTP, OTPResendCooldown
from BoardsCafe.core.email import send_email


class OTPService:
    @staticmethod
    def create_otp(user, purpose, length=None, expiry_minutes=None, max_attempts=None):
        if length is None:
            length = getattr(settings, 'OTP_LENGTH', 6)
        if expiry_minutes is None:
            expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
        if max_attempts is None:
            max_attempts = getattr(settings, 'OTP_MAX_ATTEMPTS', 3)

        OTP.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)

        otp_code = OTP.generate_otp(length)
        otp_hash = OTP.hash_otp(otp_code)
        expires_at = timezone.now() + timezone.timedelta(minutes=expiry_minutes)

        otp = OTP.objects.create(
            user=user,
            purpose=purpose,
            otp_hash=otp_hash,
            max_attempts=max_attempts,
            expires_at=expires_at,
        )

        return otp, otp_code

    @staticmethod
    def send_otp_email(user, otp_code, purpose):
        subject_map = {
            'EMAIL_VERIFICATION': 'Verify Your Email Address',
            'PASSWORD_RESET': 'Reset Your Password',
            'ACCOUNT_VERIFICATION': 'Verify Your Account',
            'LOGIN_2FA': 'Your Login Code',
        }

        subject = subject_map.get(purpose, 'Your Verification Code')
        message = f'Your verification code is: {otp_code}\n\nThis code will expire in {getattr(settings, "OTP_EXPIRY_MINUTES", 10)} minutes.'

        send_email(
            subject=subject,
            message=message,
            recipient_list=[user.email],
        )

    @staticmethod
    def verify_otp(user, otp_code, purpose):
        try:
            otp = OTP.objects.filter(
                user=user,
                purpose=purpose,
                is_used=False
            ).latest('created_at')
        except OTP.DoesNotExist:
            return False, 'No valid OTP found.'

        return otp.verify(otp_code)

    @staticmethod
    def can_resend_otp(user, purpose, cooldown_seconds=None):
        if cooldown_seconds is None:
            cooldown_seconds = getattr(settings, 'OTP_RESEND_COOLDOWN_SECONDS', 60)

        cooldown, _ = OTPResendCooldown.objects.get_or_create(
            user=user,
            purpose=purpose
        )
        return cooldown.can_resend(cooldown_seconds)

    @staticmethod
    def record_otp_sent(user, purpose):
        cooldown, _ = OTPResendCooldown.objects.get_or_create(
            user=user,
            purpose=purpose
        )
        cooldown.save()