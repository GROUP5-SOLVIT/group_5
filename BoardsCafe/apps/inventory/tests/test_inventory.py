from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from BoardsCafe.apps.inventory.models import (
    InventoryCategory, InventoryItem, StockBalance, UnitOfMeasure,
)
from BoardsCafe.apps.roles.models import Permission, Role


User = get_user_model()


class InventoryModelTests(TestCase):
    def setUp(self):
        self.category = InventoryCategory.objects.create(name='Ingredients')
        self.unit = UnitOfMeasure.objects.create(name='Kilogram', symbol='kg')

    def test_category_creation_and_case_insensitive_uniqueness(self):
        category = InventoryCategory.objects.create(name='Packaging')
        self.assertEqual(category.name, 'Packaging')
        with self.assertRaises(IntegrityError), transaction.atomic():
            InventoryCategory.objects.create(name='packaging')

    def test_unit_creation_and_duplicate_validation(self):
        unit = UnitOfMeasure.objects.create(name='Litre', symbol='L')
        self.assertEqual(unit.symbol, 'L')
        with self.assertRaises(IntegrityError), transaction.atomic():
            UnitOfMeasure.objects.create(name='liter', symbol='l')

    def test_item_relationships_and_zero_balance_initialization(self):
        item = InventoryItem.objects.create(
            name='Coffee beans', category=self.category, base_unit=self.unit,
            minimum_stock_level=Decimal('2.500'),
        )
        self.assertEqual(item.category, self.category)
        self.assertEqual(item.base_unit, self.unit)
        self.assertEqual(item.stock_balance.quantity, Decimal('0.000'))

    def test_item_requires_name_and_rejects_negative_minimum(self):
        item = InventoryItem(name=' ', category=self.category, base_unit=self.unit)
        with self.assertRaises(ValidationError):
            item.full_clean()
        item.name = 'Flour'
        item.minimum_stock_level = Decimal('-0.001')
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_duplicate_sku_is_rejected_case_insensitively(self):
        InventoryItem.objects.create(name='Item one', sku='SKU-1', category=self.category, base_unit=self.unit)
        with self.assertRaises(IntegrityError), transaction.atomic():
            InventoryItem.objects.create(name='Item two', sku='sku-1', category=self.category, base_unit=self.unit)

    def test_stock_balance_is_decimal_and_negative_values_are_rejected(self):
        item = InventoryItem.objects.create(name='Tea', category=self.category, base_unit=self.unit)
        balance = item.stock_balance
        self.assertIsInstance(balance.quantity, Decimal)
        balance.quantity = Decimal('-1.000')
        with self.assertRaises(ValidationError):
            balance.full_clean()


@override_settings(SECURE_SSL_REDIRECT=False)
class InventoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = InventoryCategory.objects.create(name='Ingredients')
        self.unit = UnitOfMeasure.objects.create(name='Piece', symbol='pc')
        self.user = User.objects.create_user(email='store@example.com', password='Cafe-Test-Password-123!')

    def grant(self, *codenames):
        role = Role.objects.create(name='Inventory test role')
        for codename in codenames:
            module, action = codename.split('.')
            permission, _ = Permission.objects.get_or_create(
                codename=codename, defaults={'module': module, 'action': action, 'name': codename},
            )
            role.permissions.add(permission)
        self.user.role = role
        self.user.save(update_fields=['role'])
        self.client.force_authenticate(user=self.user)

    def test_inventory_requires_authentication(self):
        response = self.client.get('/api/v1/inventory/items/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_without_permission_cannot_change_inventory(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/inventory/categories/', {'name': 'Drinks'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_create_list_retrieve_and_update_item(self):
        self.grant('inventory.view', 'inventory.create', 'inventory.update')
        create_response = self.client.post('/api/v1/inventory/items/', {
            'name': 'Soda bottle', 'sku': 'SODA-1', 'category': self.category.pk,
            'base_unit': self.unit.pk, 'minimum_stock_level': '4.000',
        }, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        item_id = create_response.data['id']
        self.assertEqual(create_response.data['current_stock'], '0.000')

        list_response = self.client.get('/api/v1/inventory/items/?category={}'.format(self.category.pk))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        retrieve_response = self.client.get(f'/api/v1/inventory/items/{item_id}/')
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        update_response = self.client.patch(
            f'/api/v1/inventory/items/{item_id}/', {'name': 'Soda bottle large', 'current_stock': '15'}, format='json',
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], 'Soda bottle large')
        self.assertEqual(StockBalance.objects.get(item_id=item_id).quantity, Decimal('0.000'))

    def test_item_api_rejects_negative_minimum_and_duplicate_sku(self):
        self.grant('inventory.view', 'inventory.create')
        payload = {
            'name': 'Rice', 'sku': 'RICE-1', 'category': self.category.pk,
            'base_unit': self.unit.pk, 'minimum_stock_level': '-1',
        }
        response = self.client.post('/api/v1/inventory/items/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        payload['minimum_stock_level'] = '0'
        self.assertEqual(self.client.post('/api/v1/inventory/items/', payload, format='json').status_code, status.HTTP_201_CREATED)
        payload['name'] = 'Rice second bag'
        payload['sku'] = 'rice-1'
        self.assertEqual(self.client.post('/api/v1/inventory/items/', payload, format='json').status_code, status.HTTP_400_BAD_REQUEST)

    def test_balance_api_is_read_only(self):
        self.grant('inventory.view', 'inventory.create')
        item = InventoryItem.objects.create(name='Milk', category=self.category, base_unit=self.unit)
        response = self.client.get('/api/v1/inventory/stock-balances/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['quantity'], '0.000')
        self.assertEqual(self.client.post('/api/v1/inventory/stock-balances/', {'item': item.pk, 'quantity': 10}).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
