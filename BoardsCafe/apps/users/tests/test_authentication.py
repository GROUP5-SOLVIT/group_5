from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user_normalizes_email_and_hashes_password(self):
        user = User.objects.create_user(
            email='  STAFF@Example.COM ', password='Cafe-Test-Password-123!'
        )

        self.assertEqual(user.email, 'staff@example.com')
        self.assertNotEqual(user.password, 'Cafe-Test-Password-123!')
        self.assertTrue(user.check_password('Cafe-Test-Password-123!'))

    def test_email_is_unique_case_insensitively_through_manager(self):
        User.objects.create_user(email='STAFF@example.com', password='Cafe-Test-Password-123!')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='staff@example.com', password='Cafe-Test-Password-123!')

    def test_create_superuser_sets_required_flags(self):
        user = User.objects.create_superuser(
            email='admin@example.com', password='Cafe-Test-Password-123!',
            first_name='Cafe', last_name='Admin',
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_rejects_inconsistent_flags(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com', password='Cafe-Test-Password-123!', is_staff=False
            )


class AuthenticationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = 'Cafe-Test-Password-123!'

    def register(self, **overrides):
        payload = {
            'email': 'staff@example.com',
            'first_name': 'Cafe',
            'last_name': 'Staff',
            'phone': '+250700000000',
            'password': self.password,
            'password_confirm': self.password,
        }
        payload.update(overrides)
        return self.client.post('/api/v1/auth/register/', payload, format='json')

    def test_registration_returns_profile_without_passwords(self):
        response = self.register()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'staff@example.com')
        self.assertNotIn('password', response.data)
        self.assertNotIn('password_confirm', response.data)
        self.assertTrue(User.objects.get().check_password(self.password))

    def test_registration_rejects_password_confirmation_mismatch(self):
        response = self.register(password_confirm='Different-Password-123!')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.exists())

    def test_registration_rejects_duplicate_email(self):
        self.register()
        response = self.register(email=' STAFF@EXAMPLE.COM ')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_and_refresh_issue_tokens(self):
        User.objects.create_user(email='staff@example.com', password=self.password)
        response = self.client.post(
            '/api/v1/auth/login/',
            {'email': 'STAFF@EXAMPLE.COM', 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        refresh_response = self.client.post(
            '/api/v1/auth/token/refresh/',
            {'refresh': response.data['refresh']},
            format='json',
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_login_rejects_invalid_credentials(self):
        User.objects.create_user(email='staff@example.com', password=self.password)
        response = self.client.post(
            '/api/v1/auth/login/',
            {'email': 'staff@example.com', 'password': 'wrong-password'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_rejects_inactive_user(self):
        User.objects.create_user(email='staff@example.com', password=self.password, is_active=False)
        response = self.client.post(
            '/api/v1/auth/login/',
            {'email': 'staff@example.com', 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_requires_authentication(self):
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_authenticated_profile(self):
        user = User.objects.create_user(email='staff@example.com', password=self.password)
        self.client.force_authenticate(user=user)

        response = self.client.get('/api/v1/auth/me/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
        self.assertNotIn('password', response.data)

    def test_user_model_is_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(User))
