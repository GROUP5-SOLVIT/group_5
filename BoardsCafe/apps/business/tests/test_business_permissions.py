from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from BoardsCafe.apps.roles.models import Permission, Role


User = get_user_model()


@override_settings(SECURE_SSL_REDIRECT=False)
class BusinessProfilePermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='business@example.com', password='Cafe-Test-Password-123!')

    def grant(self, *codenames):
        role = Role.objects.create(name='Business test role')
        for codename in codenames:
            module, action = codename.split('.')
            permission, _ = Permission.objects.get_or_create(
                codename=codename,
                defaults={'module': module, 'action': action, 'name': codename},
            )
            role.permissions.add(permission)
        self.user.role = role
        self.user.save(update_fields=['role'])
        self.client.force_authenticate(user=self.user)

    def test_business_list_requires_view_permission(self):
        self.grant('settings.view')

        response = self.client.get('/api/v1/business/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_create_requires_update_permission(self):
        self.grant('settings.update')

        response = self.client.post('/api/v1/business/', {'name': "Board's Cafe"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_business_create_denies_user_without_update_permission(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/v1/business/', {'name': "Board's Cafe"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
