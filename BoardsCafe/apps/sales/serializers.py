
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem


CENT = Decimal("0.01")


def money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id", "product", "variant", "product_name",
            "variant_name", "quantity", "unit_price", "line_total",
        ]
        read_only_fields = [
            "id", "product_name", "variant_name",
            "unit_price", "line_total",
        ]

    def validate(self, attrs):
        product = attrs.get(
            "product", getattr(self.instance, "product", None)
        )
        variant = attrs.get(
            "variant", getattr(self.instance, "variant", None)
        )
        quantity = attrs.get(
            "quantity", getattr(self.instance, "quantity", 1)
        )

        if product and not product.is_available:
            raise serializers.ValidationError({
                "product": "This product is unavailable."
            })

        if variant:
            if product and variant.product_id != product.id:
                raise serializers.ValidationError({
                    "variant": "The variant must belong to the selected product."
                })
            if not variant.is_available:
                raise serializers.ValidationError({
                    "variant": "This variant is unavailable."
                })

        if quantity < 1:
            raise serializers.ValidationError({
                "quantity": "Quantity must be at least 1."
            })

        return attrs


class OrderReceiptItemSerializer(serializers.Serializer):
    product = serializers.CharField()
    variant = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2)


class OrderReceiptSerializer(serializers.Serializer):
    order_number = serializers.UUIDField()
    status = serializers.ChoiceField(choices=Order.Status.choices)
    created_at = serializers.DateTimeField()
    items = OrderReceiptItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)
    discount = serializers.DecimalField(max_digits=12, decimal_places=2)
    tax = serializers.DecimalField(max_digits=12, decimal_places=2)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "created_by", "status",
            "discount_type", "discount_value", "subtotal",
            "discount_amount", "tax_amount", "total_amount",
            "notes", "items", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "order_number", "created_by", "status",
            "subtotal", "discount_amount", "tax_amount",
            "total_amount", "created_at", "updated_at",
        ]

    def validate(self, attrs):
        if self.instance and self.instance.status != Order.Status.DRAFT:
            raise serializers.ValidationError(
                "Only draft orders can be edited."
            )

        items = attrs.get("items")
        if items is None and not self.instance:
            raise serializers.ValidationError({
                "items": "At least one order item is required."
            })

        discount_type = attrs.get(
            "discount_type",
            getattr(self.instance, "discount_type", Order.DiscountType.NONE),
        )
        discount_value = attrs.get(
            "discount_value",
            getattr(self.instance, "discount_value", Decimal("0.00")),
        )

        if discount_type == Order.DiscountType.PERCENT and discount_value > 100:
            raise serializers.ValidationError({
                "discount_value": "Percentage discount cannot exceed 100."
            })

        if discount_type == Order.DiscountType.NONE and discount_value != 0:
            raise serializers.ValidationError({
                "discount_value": "Use zero when no discount is selected."
            })

        return attrs

    def _save_items(self, order, items):
        subtotal = Decimal("0.00")

        for item_data in items:
            product = item_data["product"]
            variant = item_data.get("variant")
            quantity = item_data["quantity"]

            if not product.is_available:
                raise serializers.ValidationError(
                    f"{product.name} is unavailable."
                )

            if variant:
                if variant.product_id != product.id or not variant.is_available:
                    raise serializers.ValidationError(
                        f"Invalid or unavailable variant for {product.name}."
                    )
                unit_price = product.base_price + variant.price_adjustment
                variant_name = variant.name
            else:
                unit_price = product.base_price
                variant_name = ""

            if unit_price < 0:
                raise serializers.ValidationError("Price cannot be negative.")

            unit_price = money(unit_price)
            line_total = money(unit_price * quantity)

            OrderItem.objects.create(
                order=order,
                product=product,
                variant=variant,
                product_name=product.name,
                variant_name=variant_name,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
            subtotal += line_total

        subtotal = money(subtotal)
        discount_type = order.discount_type
        discount_value = order.discount_value

        if discount_type == Order.DiscountType.FIXED:
            discount_amount = min(discount_value, subtotal)
        elif discount_type == Order.DiscountType.PERCENT:
            discount_amount = subtotal * discount_value / Decimal("100")
        else:
            discount_amount = Decimal("0.00")

        discount_amount = money(discount_amount)
        taxable_amount = max(subtotal - discount_amount, Decimal("0.00"))
        tax_amount = money(order.tax_amount)
        total = money(taxable_amount + tax_amount)

        order.subtotal = subtotal
        order.discount_amount = discount_amount
        order.total_amount = total
        order.save(update_fields=[
            "subtotal", "discount_amount", "total_amount", "updated_at"
        ])

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")
        request = self.context["request"]

        order = Order.objects.create(
            created_by=request.user,
            **validated_data,
        )
        self._save_items(order, items)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        items = validated_data.pop("items", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if items is not None:
            instance.items.all().delete()
            self._save_items(instance, items)

        return instance
