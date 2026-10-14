from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower


class InventoryCategory(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(Lower('name'), name='inventory_category_name_ci_uniq')]

    def clean(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError({'name': 'This field may not be blank.'})

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=80)
    symbol = models.CharField(max_length=24)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(Lower('name'), name='inventory_unit_name_ci_uniq'),
            models.UniqueConstraint(Lower('symbol'), name='inventory_unit_symbol_ci_uniq'),
        ]

    def clean(self):
        self.name = self.name.strip()
        self.symbol = self.symbol.strip()
        errors = {}
        if not self.name:
            errors['name'] = 'This field may not be blank.'
        if not self.symbol:
            errors['symbol'] = 'This field may not be blank.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.symbol = self.symbol.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.symbol})'


class InventoryItem(models.Model):
    name = models.CharField(max_length=160)
    sku = models.CharField(max_length=64, null=True, blank=True)
    category = models.ForeignKey(InventoryCategory, on_delete=models.PROTECT, related_name='items')
    base_unit = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT, related_name='items')
    description = models.TextField(blank=True)
    minimum_stock_level = models.DecimalField(
        max_digits=14, decimal_places=3, default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0'))],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(Lower('sku'), condition=Q(sku__isnull=False) & ~Q(sku=''), name='inventory_item_sku_ci_uniq'),
            models.CheckConstraint(condition=Q(minimum_stock_level__gte=0), name='inventory_item_min_stock_nonnegative'),
        ]

    def clean(self):
        self.name = self.name.strip()
        if self.sku is not None:
            self.sku = self.sku.strip() or None
        if not self.name:
            raise ValidationError({'name': 'This field may not be blank.'})
        if self.minimum_stock_level is not None and self.minimum_stock_level < 0:
            raise ValidationError({'minimum_stock_level': 'Minimum stock level cannot be negative.'})

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        if self.sku is not None:
            self.sku = self.sku.strip() or None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StockBalance(models.Model):
    item = models.OneToOneField(InventoryItem, on_delete=models.CASCADE, related_name='stock_balance')
    quantity = models.DecimalField(
        max_digits=14, decimal_places=3, default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0'))],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['item__name']
        constraints = [models.CheckConstraint(condition=Q(quantity__gte=0), name='inventory_stock_quantity_nonnegative')]

    def clean(self):
        if self.quantity is not None and self.quantity < 0:
            raise ValidationError({'quantity': 'Stock quantity cannot be negative.'})

    def __str__(self):
        return f'{self.item.name}: {self.quantity}'
