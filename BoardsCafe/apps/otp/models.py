import hashlib
import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone


class OTP(models.Model):
    PURPOSE_CHOICES = [
        ('EMAIL_VERIFICATION', 'Email Verification'),
        ('PASSWORD_RESET', 'Password Reset'),
        ('ACCOUNT_VERIFICATION', 'Account Verification'),
        ('LOGIN_2FA', 'Two-Factor Authentication'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='otps'
    )
    purpose = models.CharField(max_length=32, choices=PURPOSE_CHOICES)
    otp_hash = models.CharField(max_length=128)
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'purpose', 'is_used']),
        ]

    def __str__(self):
        return f'OTP for {self.user.email} - {self.purpose}'

    @classmethod
    def generate_otp(cls, length=6):
        return ''.join(secrets.choice('0123456789') for _ in range(length))

    @classmethod
    def hash_otp(cls, otp):
        return hashlib.sha256(otp.encode()).hexdigest()

    def verify(self, otp):
        if self.is_used:
            return False, 'OTP has already been used.'

        if timezone.now() > self.expires_at:
            return False, 'OTP has expired.'

        if self.attempts >= self.max_attempts:
            return False, 'Maximum verification attempts exceeded.'

        self.attempts += 1
        self.save(update_fields=['attempts'])

        if self.hash_otp(otp) != self.otp_hash:
            return False, 'Invalid OTP.'

        self.is_used = True
        self.save(update_fields=['is_used'])
        return True, 'OTP verified successfully.'


class OTPResendCooldown(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='otp_cooldowns'
    )
    purpose = models.CharField(max_length=32, choices=OTP.PURPOSE_CHOICES)
    last_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'purpose']

    def __str__(self):
        return f'Cooldown for {self.user.email} - {self.purpose}'

    def can_resend(self, cooldown_seconds=60):
        if not self.last_sent_at:
            return True
        elapsed = (timezone.now() - self.last_sent_at).total_seconds()
        return elapsed >= cooldown_seconds

    def remaining_cooldown(self, cooldown_seconds=60):
        if not self.last_sent_at:
            return 0
        elapsed = (timezone.now() - self.last_sent_at).total_seconds()
        remaining = cooldown_seconds - elapsed
        return max(0, int(remaining))