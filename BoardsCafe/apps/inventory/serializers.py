from rest_framework import serializers

from .models import InventoryCategory, InventoryItem, StockBalance, UnitOfMeasure


class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = ('id', 'name', 'description', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_name(self, value):
        value = value.strip()
        qs = InventoryCategory.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A category with this name already exists.')
        return value


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ('id', 'name', 'symbol', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_name(self, value):
        value = value.strip()
        qs = UnitOfMeasure.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A unit with this name already exists.')
        return value

    def validate_symbol(self, value):
        value = value.strip()
        qs = UnitOfMeasure.objects.filter(symbol__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A unit with this symbol already exists.')
        return value


class InventoryItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    base_unit_name = serializers.CharField(source='base_unit.name', read_only=True)
    base_unit_symbol = serializers.CharField(source='base_unit.symbol', read_only=True)
    current_stock = serializers.DecimalField(source='stock_balance.quantity', max_digits=14, decimal_places=3, read_only=True)

    class Meta:
        model = InventoryItem
        fields = (
            'id', 'name', 'sku', 'category', 'category_name', 'base_unit', 'base_unit_name',
            'base_unit_symbol', 'description', 'minimum_stock_level', 'is_active',
            'current_stock', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'current_stock', 'created_at', 'updated_at')

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('This field may not be blank.')
        return value

    def validate_sku(self, value):
        value = value.strip() if value else None
        if not value:
            return None
        qs = InventoryItem.objects.filter(sku__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('An item with this SKU already exists.')
        return value

    def validate_minimum_stock_level(self, value):
        if value < 0:
            raise serializers.ValidationError('Minimum stock level cannot be negative.')
        return value


class StockBalanceSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    unit_symbol = serializers.CharField(source='item.base_unit.symbol', read_only=True)

    class Meta:
        model = StockBalance
        fields = ('id', 'item', 'item_name', 'unit_symbol', 'quantity', 'created_at', 'updated_at')
        read_only_fields = fields
