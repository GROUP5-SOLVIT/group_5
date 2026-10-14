from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from BoardsCafe.apps.purchasing.models import Purchase
from BoardsCafe.apps.sales.models import Order

from .models import Expense, ExpenseCategory, Payment


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = (
            "id", "category", "category_name", "description", "amount",
            "expense_date", "payment_method", "reference", "vendor",
            "notes", "created_by", "created_at", "updated_at",
        )
        read_only_fields = ("id", "category_name", "created_by", "created_at", "updated_at")

    def validate_category(self, value):
        if not value.is_active:
            raise serializers.ValidationError("An inactive category cannot be used.")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.UUIDField(source="order.order_number", read_only=True)
    purchase_number = serializers.UUIDField(source="purchase.purchase_number", read_only=True)
    source_type = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            "id", "order", "order_number", "purchase", "purchase_number",
            "source_type", "amount", "payment_method", "reference", "status",
            "paid_at", "recorded_by", "notes", "created_at",
        )
        read_only_fields = (
            "id", "order_number", "purchase_number", "source_type",
            "recorded_by", "paid_at", "created_at",
        )

    @extend_schema_field(OpenApiTypes.STR)
    def get_source_type(self, obj):
        return "customer" if obj.order_id else "supplier"

    def validate(self, attrs):
        order = attrs.get("order", getattr(self.instance, "order", None))
        purchase = attrs.get("purchase", getattr(self.instance, "purchase", None))
        if (order is None) == (purchase is None):
            raise serializers.ValidationError(
                "A payment must be linked to exactly one order or purchase."
            )
        if self.instance:
            raise serializers.ValidationError("Payment records are immutable.")

        amount = attrs.get("amount", Decimal("0.00"))
        status = attrs.get("status", Payment.Status.COMPLETED)
        if status == Payment.Status.COMPLETED:
            if order:
                if order.status not in (Order.Status.PENDING, Order.Status.PAID):
                    raise serializers.ValidationError({
                        "order": "Payments can be recorded only for pending or paid orders."
                    })
                already_paid = order.payments.filter(
                    status=Payment.Status.COMPLETED,
                ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
                if already_paid + amount > order.total_amount:
                    raise serializers.ValidationError({
                        "amount": "Payment exceeds the order's outstanding balance."
                    })
            else:
                if purchase.status not in (
                    Purchase.Status.PARTIALLY_RECEIVED,
                    Purchase.Status.RECEIVED,
                ):
                    raise serializers.ValidationError({
                        "purchase": "Supplier payments require a received purchase."
                    })
                already_paid = purchase.payments.filter(
                    status=Payment.Status.COMPLETED,
                ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
                if already_paid + amount > purchase.total_amount:
                    raise serializers.ValidationError({
                        "amount": "Payment exceeds the purchase's outstanding balance."
                    })
        return attrs

    def create(self, validated_data):
        payment = Payment.objects.create(
            recorded_by=self.context["request"].user,
            paid_at=timezone.now() if validated_data.get("status", Payment.Status.COMPLETED) == Payment.Status.COMPLETED else None,
            **validated_data,
        )
        if payment.order_id and payment.status == Payment.Status.COMPLETED:
            paid = payment.order.payments.filter(
                status=Payment.Status.COMPLETED,
            ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
            if paid >= payment.order.total_amount:
                payment.order.status = Order.Status.PAID
                payment.order.save(update_fields=["status", "updated_at"])
        return payment
