from decimal import Decimal

from rest_framework import serializers

from BoardsCafe.apps.inventory.models import InventoryItem

from .models import (
    Purchase,
    PurchaseItem,
    PurchaseReceipt,
    PurchaseReceiptItem,
    Supplier,
)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            "id", "name", "contact_person", "phone", "email", "address",
            "tax_id", "status", "notes", "created_by", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")


class PurchaseItemInputSerializer(serializers.ModelSerializer):
    inventory_item_name = serializers.CharField(
        source="inventory_item.name",
        read_only=True,
    )
    unit_symbol = serializers.CharField(
        source="inventory_item.base_unit.symbol",
        read_only=True,
    )
    line_total = serializers.DecimalField(
        max_digits=16,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = PurchaseItem
        fields = (
            "id", "inventory_item", "inventory_item_name", "unit_symbol",
            "ordered_quantity", "received_quantity", "unit_cost", "line_total",
            "notes",
        )
        read_only_fields = ("id", "inventory_item_name", "unit_symbol", "received_quantity", "line_total")

    def validate_inventory_item(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Inactive inventory items cannot be purchased.")
        return value


class PurchaseSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    items = PurchaseItemInputSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=16,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Purchase
        fields = (
            "id", "purchase_number", "supplier", "supplier_name",
            "purchase_date", "expected_delivery_date", "supplier_invoice",
            "status", "items", "total_amount", "notes", "created_by",
            "ordered_at", "received_at", "created_at", "updated_at",
        )
        read_only_fields = (
            "id", "purchase_number", "supplier_name", "status", "items",
            "total_amount", "created_by", "ordered_at", "received_at",
            "created_at", "updated_at",
        )


class PurchaseWriteSerializer(serializers.ModelSerializer):
    items = PurchaseItemInputSerializer(many=True, required=True)

    class Meta:
        model = Purchase
        fields = (
            "id", "supplier", "purchase_date", "expected_delivery_date",
            "supplier_invoice", "items", "notes",
        )
        read_only_fields = ("id",)

    def validate_supplier(self, value):
        if value.status != Supplier.Status.ACTIVE:
            raise serializers.ValidationError("Only active suppliers can be used for purchases.")
        return value

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("A purchase must contain at least one item.")
        item_ids = [item["inventory_item"].pk for item in items]
        if len(item_ids) != len(set(item_ids)):
            raise serializers.ValidationError("Each inventory item may appear only once.")
        return items

    def create(self, validated_data):
        items = validated_data.pop("items")
        purchase = Purchase.objects.create(
            created_by=self.context["request"].user,
            **validated_data,
        )
        PurchaseItem.objects.bulk_create([
            PurchaseItem(purchase=purchase, **item)
            for item in items
        ])
        return purchase

    def update(self, instance, validated_data):
        items = validated_data.pop("items", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if items is not None:
            instance.items.all().delete()
            PurchaseItem.objects.bulk_create([
                PurchaseItem(purchase=instance, **item)
                for item in items
            ])
        return instance


class PurchaseReceiptItemInputSerializer(serializers.Serializer):
    purchase_item = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseItem.objects.select_related("inventory_item").all(),
    )
    batch_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    quantity_received = serializers.DecimalField(
        max_digits=14,
        decimal_places=3,
        min_value=Decimal("0.001"),
    )
    unit_cost = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        required=False,
    )
    expiry_date = serializers.DateField(required=False, allow_null=True)


class PurchaseReceiptRequestSerializer(serializers.Serializer):
    items = PurchaseReceiptItemInputSerializer(many=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one received item is required.")
        return items


class PurchaseReceiptItemSerializer(serializers.ModelSerializer):
    inventory_item_name = serializers.CharField(
        source="purchase_item.inventory_item.name",
        read_only=True,
    )

    class Meta:
        model = PurchaseReceiptItem
        fields = (
            "id", "purchase_item", "inventory_item_name", "batch_number",
            "quantity_received", "unit_cost", "expiry_date",
        )
        read_only_fields = fields


class PurchaseReceiptSerializer(serializers.ModelSerializer):
    items = PurchaseReceiptItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseReceipt
        fields = ("id", "purchase", "received_by", "received_at", "notes", "items")
        read_only_fields = fields
