from decimal import Decimal

from django.db.models import Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, extend_schema

from BoardsCafe.apps.finance.models import Expense, Payment
from BoardsCafe.apps.inventory.models import StockBalance
from BoardsCafe.apps.purchasing.models import PurchaseItem
from BoardsCafe.apps.sales.models import Order
from BoardsCafe.core.permissions import dashboard_view
from BoardsCafe.core.throttling import AuthRateThrottle

from .serializers import DashboardQuerySerializer, DashboardSerializer


ZERO = Decimal("0.00")


@extend_schema(
    tags=["dashboard"],
    summary="Get a live operational dashboard summary",
    parameters=[
        OpenApiParameter("period", str, OpenApiParameter.QUERY, enum=["today", "yesterday", "this_week", "this_month", "custom"]),
        OpenApiParameter("date_from", str, OpenApiParameter.QUERY, description="Required with period=custom."),
        OpenApiParameter("date_to", str, OpenApiParameter.QUERY, description="Required with period=custom."),
    ],
    responses=DashboardSerializer,
)
class DashboardSummaryView(APIView):
    throttle_classes = [AuthRateThrottle]
    permission_classes = [permissions.IsAuthenticated, dashboard_view]

    def get(self, request):
        query = DashboardQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        date_from = query.validated_data["date_from"]
        date_to = query.validated_data["date_to"]

        orders = Order.objects.filter(created_at__date__range=(date_from, date_to))
        paid_orders = orders.filter(status=Order.Status.PAID)
        customer_payments = Payment.objects.filter(
            status=Payment.Status.COMPLETED,
            order__isnull=False,
            paid_at__date__range=(date_from, date_to),
        )
        expenses = Expense.objects.filter(expense_date__range=(date_from, date_to))
        purchase_items = PurchaseItem.objects.filter(purchase__purchase_date__range=(date_from, date_to))
        balances = StockBalance.objects.select_related("item").filter(item__is_active=True)

        low_stock_count = 0
        out_of_stock_count = 0
        for balance in balances:
            if balance.quantity <= 0:
                out_of_stock_count += 1
            elif balance.quantity <= balance.item.minimum_stock_level:
                low_stock_count += 1

        paid_sales = paid_orders.aggregate(total=Sum("total_amount"))["total"] or ZERO
        purchase_total = sum(
            (item.ordered_quantity * item.unit_cost for item in purchase_items),
            ZERO,
        )
        payload = {
            "period_start": date_from,
            "period_end": date_to,
            "total_sales": paid_sales,
            "customer_payments": customer_payments.aggregate(total=Sum("amount"))["total"] or ZERO,
            "order_count": orders.count(),
            "paid_order_count": paid_orders.count(),
            "pending_order_count": orders.filter(status=Order.Status.PENDING).count(),
            "average_order_value": paid_sales / paid_orders.count() if paid_orders.exists() else ZERO,
            "total_expenses": expenses.aggregate(total=Sum("amount"))["total"] or ZERO,
            "purchase_total": purchase_total,
            "purchase_count": purchase_items.values("purchase_id").distinct().count(),
            "total_inventory_items": balances.count(),
            "low_stock_item_count": low_stock_count,
            "out_of_stock_item_count": out_of_stock_count,
        }
        return Response(DashboardSerializer(payload).data)
