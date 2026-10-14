from decimal import Decimal

from django.db.models import Count, DecimalField, F, Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, extend_schema

from BoardsCafe.apps.finance.models import Expense, Payment
from BoardsCafe.apps.inventory.models import StockBalance
from BoardsCafe.apps.purchasing.models import Purchase, PurchaseItem
from BoardsCafe.apps.sales.models import Order, OrderItem
from BoardsCafe.core.permissions import reports_view
from BoardsCafe.core.throttling import AuthRateThrottle

from .serializers import (
    DateRangeQuerySerializer,
    ExpenseReportSerializer,
    InventoryReportSerializer,
    PurchaseReportSerializer,
    SalesReportSerializer,
)


ZERO = Decimal("0.00")


class ReportPermissionMixin:
    throttle_classes = [AuthRateThrottle]
    permission_classes = [permissions.IsAuthenticated, reports_view]

    def date_range(self):
        serializer = DateRangeQuerySerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


def apply_date_range(queryset, field_name, date_range):
    if date_range.get("date_from"):
        queryset = queryset.filter(**{f"{field_name}__gte": date_range["date_from"]})
    if date_range.get("date_to"):
        queryset = queryset.filter(**{f"{field_name}__lte": date_range["date_to"]})
    return queryset


@extend_schema(
    tags=["reports"],
    summary="Sales report",
    description="Summarises order and completed-payment activity over an optional date range.",
    parameters=[
        OpenApiParameter("date_from", str, OpenApiParameter.QUERY, description="ISO-8601 start date."),
        OpenApiParameter("date_to", str, OpenApiParameter.QUERY, description="ISO-8601 end date."),
    ],
    responses=SalesReportSerializer,
)
class SalesReportView(ReportPermissionMixin, APIView):
    def get(self, request):
        date_range = self.date_range()
        orders = apply_date_range(Order.objects.all(), "created_at__date", date_range)
        paid_orders = orders.filter(status=Order.Status.PAID)
        completed_payments = apply_date_range(
            Payment.objects.filter(status=Payment.Status.COMPLETED, order__isnull=False),
            "paid_at__date",
            date_range,
        )
        paid_items = OrderItem.objects.filter(order__in=paid_orders)

        product_rows = paid_items.values("product_id", "product_name").annotate(
            quantity_sold=Sum("quantity"), sales=Sum("line_total")
        ).order_by("-sales", "product_name")
        category_rows = paid_items.values("product__category_id", "product__category__name").annotate(
            quantity_sold=Sum("quantity"), sales=Sum("line_total")
        ).order_by("-sales", "product__category__name")
        payment_rows = completed_payments.values("payment_method").annotate(
            total=Sum("amount")
        ).order_by("payment_method")

        paid_order_total = paid_orders.aggregate(total=Sum("total_amount"))["total"] or ZERO
        payload = {
            "total_orders": orders.count(),
            "paid_orders": paid_orders.count(),
            "cancelled_orders": orders.filter(status=Order.Status.CANCELLED).count(),
            "total_sales": paid_order_total,
            "total_paid": completed_payments.aggregate(total=Sum("amount"))["total"] or ZERO,
            "average_order_value": paid_order_total / paid_orders.count() if paid_orders.exists() else ZERO,
            "sales_by_product": [
                {
                    "product_id": row["product_id"],
                    "product_name": row["product_name"],
                    "quantity_sold": row["quantity_sold"],
                    "sales": row["sales"],
                }
                for row in product_rows
            ],
            "sales_by_category": [
                {
                    "category_id": row["product__category_id"],
                    "category_name": row["product__category__name"],
                    "quantity_sold": row["quantity_sold"],
                    "sales": row["sales"],
                }
                for row in category_rows
            ],
            "payments_by_method": list(payment_rows),
        }
        return Response(SalesReportSerializer(payload).data)


@extend_schema(
    tags=["reports"],
    summary="Inventory report",
    description="Shows current stock, including low and out-of-stock items.",
    responses=InventoryReportSerializer,
)
class InventoryReportView(ReportPermissionMixin, APIView):
    def get(self, request):
        balances = StockBalance.objects.select_related("item__category", "item__base_unit").filter(item__is_active=True)
        items = []
        low_stock = 0
        out_of_stock = 0
        for balance in balances:
            if balance.quantity <= 0:
                stock_status = "out_of_stock"
                out_of_stock += 1
            elif balance.quantity <= balance.item.minimum_stock_level:
                stock_status = "low"
                low_stock += 1
            else:
                stock_status = "normal"
            items.append({
                "item_id": balance.item_id,
                "item_name": balance.item.name,
                "category": balance.item.category.name,
                "unit": balance.item.base_unit.symbol,
                "quantity": balance.quantity,
                "minimum_stock_level": balance.item.minimum_stock_level,
                "status": stock_status,
            })
        return Response(InventoryReportSerializer({
            "total_items": len(items),
            "low_stock_items": low_stock,
            "out_of_stock_items": out_of_stock,
            "items": items,
        }).data)


@extend_schema(
    tags=["reports"],
    summary="Expense report",
    parameters=[
        OpenApiParameter("date_from", str, OpenApiParameter.QUERY, description="ISO-8601 start date."),
        OpenApiParameter("date_to", str, OpenApiParameter.QUERY, description="ISO-8601 end date."),
    ],
    responses=ExpenseReportSerializer,
)
class ExpenseReportView(ReportPermissionMixin, APIView):
    def get(self, request):
        expenses = apply_date_range(Expense.objects.all(), "expense_date", self.date_range())
        category_rows = expenses.values("category_id", "category__name").annotate(
            total=Sum("amount")
        ).order_by("-total", "category__name")
        return Response(ExpenseReportSerializer({
            "total_expenses": expenses.aggregate(total=Sum("amount"))["total"] or ZERO,
            "expense_count": expenses.count(),
            "expenses_by_category": [
                {
                    "category_id": row["category_id"],
                    "category_name": row["category__name"],
                    "total": row["total"],
                }
                for row in category_rows
            ],
        }).data)


@extend_schema(
    tags=["reports"],
    summary="Purchase report",
    parameters=[
        OpenApiParameter("date_from", str, OpenApiParameter.QUERY, description="ISO-8601 start date."),
        OpenApiParameter("date_to", str, OpenApiParameter.QUERY, description="ISO-8601 end date."),
    ],
    responses=PurchaseReportSerializer,
)
class PurchaseReportView(ReportPermissionMixin, APIView):
    def get(self, request):
        purchases = apply_date_range(Purchase.objects.all(), "purchase_date", self.date_range())
        amount_expression = Sum(
            F("ordered_quantity") * F("unit_cost"),
            output_field=DecimalField(max_digits=16, decimal_places=2),
        )
        supplier_rows = PurchaseItem.objects.filter(purchase__in=purchases).values(
            "purchase__supplier_id", "purchase__supplier__name"
        ).annotate(
            purchase_count=Count("purchase_id", distinct=True),
            total=amount_expression,
        ).order_by("-total", "purchase__supplier__name")
        return Response(PurchaseReportSerializer({
            "purchase_count": purchases.count(),
            "total_purchases": PurchaseItem.objects.filter(purchase__in=purchases).aggregate(total=amount_expression)["total"] or ZERO,
            "draft_count": purchases.filter(status=Purchase.Status.DRAFT).count(),
            "ordered_count": purchases.filter(status=Purchase.Status.ORDERED).count(),
            "partially_received_count": purchases.filter(status=Purchase.Status.PARTIALLY_RECEIVED).count(),
            "received_count": purchases.filter(status=Purchase.Status.RECEIVED).count(),
            "purchases_by_supplier": [
                {
                    "supplier_id": row["purchase__supplier_id"],
                    "supplier_name": row["purchase__supplier__name"],
                    "purchase_count": row["purchase_count"],
                    "total": row["total"],
                }
                for row in supplier_rows
            ],
        }).data)
