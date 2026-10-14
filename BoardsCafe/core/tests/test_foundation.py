from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from django.utils import timezone

from BoardsCafe.apps.otp.models import OTP, OTPResendCooldown
from BoardsCafe.apps.otp.services import OTPService
from BoardsCafe.core.pagination import StandardResultsSetPagination
from BoardsCafe.core.responses import success_response, error_response

User = get_user_model()


class PaginationTests(TestCase):
    def test_pagination_class_exists(self):
        pagination = StandardResultsSetPagination()
        self.assertEqual(pagination.page_size, 20)
        self.assertEqual(pagination.max_page_size, 100)
        self.assertEqual(pagination.page_size_query_param, 'page_size')


class ResponseFormatTests(TestCase):
    def test_success_response(self):
        response = success_response(data={'test': 'data'}, message='Test success')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Test success')
        self.assertEqual(response.data['data'], {'test': 'data'})

    def test_error_response(self):
        response = error_response(message='Test error', errors={'field': 'error'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'Test error')
        self.assertEqual(response.data['errors'], {'field': 'error'})

    def test_created_response(self):
        from BoardsCafe.core.responses import created_response
        response = created_response(data={'id': 1}, message='Created')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])

    def test_no_content_response(self):
        from BoardsCafe.core.responses import no_content_response
        response = no_content_response()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OTPModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

    def test_generate_otp(self):
        otp = OTP.generate_otp(6)
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

    def test_hash_otp(self):
        otp = '123456'
        hashed = OTP.hash_otp(otp)
        self.assertEqual(len(hashed), 64)
        self.assertEqual(hashed, OTP.hash_otp(otp))

    def test_create_otp(self):
        otp, code = OTPService.create_otp(self.user, 'EMAIL_VERIFICATION')
        self.assertEqual(otp.user, self.user)
        self.assertEqual(otp.purpose, 'EMAIL_VERIFICATION')
        self.assertFalse(otp.is_used)
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

    def test_verify_otp_success(self):
        otp, code = OTPService.create_otp(self.user, 'EMAIL_VERIFICATION')
        is_valid, message = OTPService.verify_otp(self.user, code, 'EMAIL_VERIFICATION')
        self.assertTrue(is_valid)
        self.assertEqual(message, 'OTP verified successfully.')
        otp.refresh_from_db()
        self.assertTrue(otp.is_used)

    def test_verify_otp_invalid(self):
        otp, _ = OTPService.create_otp(self.user, 'EMAIL_VERIFICATION')
        is_valid, message = OTPService.verify_otp(self.user, '000000', 'EMAIL_VERIFICATION')
        self.assertFalse(is_valid)
        self.assertEqual(message, 'Invalid OTP.')

    def test_verify_otp_expired(self):
        from django.utils import timezone
        otp, code = OTPService.create_otp(self.user, 'EMAIL_VERIFICATION', expiry_minutes=0)
        otp.expires_at = timezone.now() - timezone.timedelta(minutes=1)
        otp.save()
        is_valid, message = OTPService.verify_otp(self.user, code, 'EMAIL_VERIFICATION')
        self.assertFalse(is_valid)
        self.assertEqual(message, 'OTP has expired.')

    def test_verify_otp_max_attempts(self):
        otp, _ = OTPService.create_otp(self.user, 'EMAIL_VERIFICATION', max_attempts=2)
        OTPService.verify_otp(self.user, '000000', 'EMAIL_VERIFICATION')
        OTPService.verify_otp(self.user, '000000', 'EMAIL_VERIFICATION')
        is_valid, message = OTPService.verify_otp(self.user, '000000', 'EMAIL_VERIFICATION')
        self.assertFalse(is_valid)
        self.assertEqual(message, 'Maximum verification attempts exceeded.')

    def test_verify_used_otp(self):
        otp, code = OTPService.create_otp(self.user, 'EMAIL_VERIFICATION')
        OTPService.verify_otp(self.user, code, 'EMAIL_VERIFICATION')
        # After verification, the OTP is marked as used, so next verification fails
        is_valid, message = OTPService.verify_otp(self.user, code, 'EMAIL_VERIFICATION')
        self.assertFalse(is_valid)
        self.assertEqual(message, 'No valid OTP found.')

    def test_resend_cooldown(self):
        from django.utils import timezone
        cooldown = OTPResendCooldown.objects.create(user=self.user, purpose='EMAIL_VERIFICATION')
        # auto_now=True sets last_sent_at on creation, so we need to set it to a past time
        cooldown.last_sent_at = timezone.now() - timezone.timedelta(seconds=120)
        cooldown.save(update_fields=['last_sent_at'])
        self.assertTrue(cooldown.can_resend(60))
        cooldown.last_sent_at = timezone.now()
        cooldown.save(update_fields=['last_sent_at'])
        self.assertFalse(cooldown.can_resend(60))
        self.assertGreater(cooldown.remaining_cooldown(60), 0)


class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_check_endpoint(self):
        response = self.client.get('/api/v1/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], "Board's Cafe API is running.")
        self.assertIn('data', response.data)
        self.assertIn('status', response.data['data'])


class AuthenticationConfigurationTests(TestCase):
    def test_jwt_settings_exist(self):
        from django.conf import settings
        self.assertIn('SIMPLE_JWT', dir(settings))
        self.assertIn('ACCESS_TOKEN_LIFETIME', settings.SIMPLE_JWT)
        self.assertIn('REFRESH_TOKEN_LIFETIME', settings.SIMPLE_JWT)
        self.assertIn('ROTATE_REFRESH_TOKENS', settings.SIMPLE_JWT)
        self.assertTrue(settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS'])
        self.assertTrue(settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION'])

    def test_drf_settings(self):
        from django.conf import settings
        self.assertEqual(settings.REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'], ['rest_framework.permissions.IsAuthenticated'])
        self.assertEqual(settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'], ['rest_framework_simplejwt.authentication.JWTAuthentication'])
        self.assertIn('DEFAULT_PAGINATION_CLASS', settings.REST_FRAMEWORK)
        self.assertIn('EXCEPTION_HANDLER', settings.REST_FRAMEWORK)
        self.assertIn('DEFAULT_THROTTLE_CLASSES', settings.REST_FRAMEWORK)
        self.assertIn('DEFAULT_THROTTLE_RATES', settings.REST_FRAMEWORK)

    def test_swagger_settings(self):
        from django.conf import settings
        self.assertIn('SPECTACULAR_SETTINGS', dir(settings))
        self.assertEqual(settings.SPECTACULAR_SETTINGS['TITLE'], "Board's Cafe API")
        self.assertIn('SECURITY', settings.SPECTACULAR_SETTINGS)
        self.assertIn('Bearer', str(settings.SPECTACULAR_SETTINGS['SECURITY']))


class EnvironmentConfigurationTests(TestCase):
    def test_env_variables_loaded(self):
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'OTP_LENGTH'))
        self.assertTrue(hasattr(settings, 'OTP_EXPIRY_MINUTES'))
        self.assertTrue(hasattr(settings, 'OTP_MAX_ATTEMPTS'))
        self.assertTrue(hasattr(settings, 'OTP_RESEND_COOLDOWN_SECONDS'))
        self.assertTrue(hasattr(settings, 'JWT_ACCESS_TOKEN_LIFETIME'))
        self.assertTrue(hasattr(settings, 'JWT_REFRESH_TOKEN_LIFETIME'))
        self.assertTrue(hasattr(settings, 'CORS_ALLOWED_ORIGINS'))


class CORSConfigurationTests(TestCase):
    def test_cors_settings(self):
        from django.conf import settings
        self.assertFalse(settings.CORS_ALLOW_ALL_ORIGINS)
        self.assertTrue(settings.CORS_ALLOW_CREDENTIALS)
        self.assertIsInstance(settings.CORS_ALLOWED_ORIGINS, list)


class SecuritySettingsTests(TestCase):
    def test_security_headers(self):
        from django.conf import settings
        self.assertTrue(settings.SECURE_BROWSER_XSS_FILTER)
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY')

    def test_password_validators(self):
        from django.conf import settings
        validators = settings.AUTH_PASSWORD_VALIDATORS
        self.assertEqual(len(validators), 4)
        validator_names = [v['NAME'] for v in validators]
        self.assertIn('django.contrib.auth.password_validation.UserAttributeSimilarityValidator', validator_names)
        self.assertIn('django.contrib.auth.password_validation.MinimumLengthValidator', validator_names)
        self.assertIn('django.contrib.auth.password_validation.CommonPasswordValidator', validator_names)
        self.assertIn('django.contrib.auth.password_validation.NumericPasswordValidator', validator_names)


class LoggingConfigurationTests(TestCase):
    def test_logging_config(self):
        from django.conf import settings
        self.assertIn('LOGGING', dir(settings))
        self.assertIn('handlers', settings.LOGGING)
        self.assertIn('console', settings.LOGGING['handlers'])
        self.assertIn('file', settings.LOGGING['handlers'])
        self.assertIn('security_file', settings.LOGGING['handlers'])
        self.assertIn('loggers', settings.LOGGING)
        self.assertIn('django.security', settings.LOGGING['loggers'])


class SwaggerSchemaTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_schema_endpoint(self):
        response = self.client.get('/api/v1/schema/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger_ui_endpoint(self):
        response = self.client.get('/api/v1/docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_endpoint(self):
        response = self.client.get('/api/v1/redoc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)