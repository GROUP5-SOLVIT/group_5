from rest_framework import serializers


class DateRangeQuerySerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, attrs):
        if attrs.get("date_from") and attrs.get("date_to") and attrs["date_from"] > attrs["date_to"]:
            raise serializers.ValidationError({"date_to": "date_to must be on or after date_from."})
        return attrs


class SalesByProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    quantity_sold = serializers.IntegerField()
    sales = serializers.DecimalField(max_digits=16, decimal_places=2)


class SalesByCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    quantity_sold = serializers.IntegerField()
    sales = serializers.DecimalField(max_digits=16, decimal_places=2)


class PaymentMethodTotalSerializer(serializers.Serializer):
    payment_method = serializers.CharField()
    total = serializers.DecimalField(max_digits=16, decimal_places=2)


class SalesReportSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    paid_orders = serializers.IntegerField()
    cancelled_orders = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=16, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=16, decimal_places=2)
    average_order_value = serializers.DecimalField(max_digits=16, decimal_places=2)
    sales_by_product = SalesByProductSerializer(many=True)
    sales_by_category = SalesByCategorySerializer(many=True)
    payments_by_method = PaymentMethodTotalSerializer(many=True)


class InventoryReportItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    item_name = serializers.CharField()
    category = serializers.CharField()
    unit = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=14, decimal_places=3)
    minimum_stock_level = serializers.DecimalField(max_digits=14, decimal_places=3)
    status = serializers.ChoiceField(choices=["normal", "low", "out_of_stock"])


class InventoryReportSerializer(serializers.Serializer):
    total_items = serializers.IntegerField()
    low_stock_items = serializers.IntegerField()
    out_of_stock_items = serializers.IntegerField()
    items = InventoryReportItemSerializer(many=True)


class ExpenseCategoryTotalSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    total = serializers.DecimalField(max_digits=16, decimal_places=2)


class ExpenseReportSerializer(serializers.Serializer):
    total_expenses = serializers.DecimalField(max_digits=16, decimal_places=2)
    expense_count = serializers.IntegerField()
    expenses_by_category = ExpenseCategoryTotalSerializer(many=True)


class SupplierPurchaseTotalSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    supplier_name = serializers.CharField()
    purchase_count = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=16, decimal_places=2)


class PurchaseReportSerializer(serializers.Serializer):
    purchase_count = serializers.IntegerField()
    total_purchases = serializers.DecimalField(max_digits=16, decimal_places=2)
    draft_count = serializers.IntegerField()
    ordered_count = serializers.IntegerField()
    partially_received_count = serializers.IntegerField()
    received_count = serializers.IntegerField()
    purchases_by_supplier = SupplierPurchaseTotalSerializer(many=True)
