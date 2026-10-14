from datetime import timedelta

from django.db import models
from django.utils import timezone
from rest_framework import serializers


class DashboardQuerySerializer(serializers.Serializer):
    class Period(models.TextChoices):
        TODAY = "today", "Today"
        YESTERDAY = "yesterday", "Yesterday"
        THIS_WEEK = "this_week", "This week"
        THIS_MONTH = "this_month", "This month"
        CUSTOM = "custom", "Custom"

    period = serializers.ChoiceField(choices=Period.choices, required=False, default=Period.TODAY)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, attrs):
        period = attrs["period"]
        today = timezone.localdate()
        if period == self.Period.CUSTOM:
            if not attrs.get("date_from") or not attrs.get("date_to"):
                raise serializers.ValidationError("Custom periods require both date_from and date_to.")
        elif period == self.Period.TODAY:
            attrs["date_from"] = attrs["date_to"] = today
        elif period == self.Period.YESTERDAY:
            attrs["date_from"] = attrs["date_to"] = today - timedelta(days=1)
        elif period == self.Period.THIS_WEEK:
            attrs["date_from"] = today - timedelta(days=today.weekday())
            attrs["date_to"] = today
        elif period == self.Period.THIS_MONTH:
            attrs["date_from"] = today.replace(day=1)
            attrs["date_to"] = today

        if attrs["date_from"] > attrs["date_to"]:
            raise serializers.ValidationError({"date_to": "date_to must be on or after date_from."})
        return attrs


class DashboardSerializer(serializers.Serializer):
    period_start = serializers.DateField()
    period_end = serializers.DateField()
    total_sales = serializers.DecimalField(max_digits=16, decimal_places=2)
    customer_payments = serializers.DecimalField(max_digits=16, decimal_places=2)
    order_count = serializers.IntegerField()
    paid_order_count = serializers.IntegerField()
    pending_order_count = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=16, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=16, decimal_places=2)
    purchase_total = serializers.DecimalField(max_digits=16, decimal_places=2)
    purchase_count = serializers.IntegerField()
    total_inventory_items = serializers.IntegerField()
    low_stock_item_count = serializers.IntegerField()
    out_of_stock_item_count = serializers.IntegerField()
