from rest_framework import mixins, permissions, viewsets
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view

from BoardsCafe.core.permissions import (
    finance_create,
    finance_delete,
    finance_update,
    finance_view,
)
from BoardsCafe.core.throttling import AuthRateThrottle

from .models import Expense, ExpenseCategory, Payment
from .serializers import ExpenseCategorySerializer, ExpenseSerializer, PaymentSerializer


class FinancePermissionMixin:
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        method = self.request.method
        if method == "POST":
            required_permission = finance_create
        elif method in ("PUT", "PATCH"):
            required_permission = finance_update
        elif method == "DELETE":
            required_permission = finance_delete
        else:
            required_permission = finance_view
        return [permissions.IsAuthenticated(), required_permission()]


@extend_schema_view(
    list=extend_schema(tags=["finance"], summary="List expense categories", responses=ExpenseCategorySerializer(many=True)),
    create=extend_schema(tags=["finance"], summary="Create an expense category", request=ExpenseCategorySerializer, responses={201: ExpenseCategorySerializer}),
    retrieve=extend_schema(tags=["finance"], summary="Retrieve an expense category", responses=ExpenseCategorySerializer),
    update=extend_schema(tags=["finance"], summary="Replace an expense category", request=ExpenseCategorySerializer, responses=ExpenseCategorySerializer),
    partial_update=extend_schema(tags=["finance"], summary="Partially update an expense category", request=ExpenseCategorySerializer, responses=ExpenseCategorySerializer),
    destroy=extend_schema(tags=["finance"], summary="Delete an unused expense category", responses={204: OpenApiResponse(description="Expense category deleted.")}),
)
class ExpenseCategoryViewSet(FinancePermissionMixin, viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() in ("true", "1", "yes"))
        return queryset


@extend_schema_view(
    list=extend_schema(
        tags=["finance"],
        summary="List expenses",
        parameters=[
            OpenApiParameter("category", int, OpenApiParameter.QUERY),
            OpenApiParameter("date_from", str, OpenApiParameter.QUERY, description="ISO-8601 start date."),
            OpenApiParameter("date_to", str, OpenApiParameter.QUERY, description="ISO-8601 end date."),
        ],
        responses=ExpenseSerializer(many=True),
    ),
    create=extend_schema(tags=["finance"], summary="Record an expense", request=ExpenseSerializer, responses={201: ExpenseSerializer}),
    retrieve=extend_schema(tags=["finance"], summary="Retrieve an expense", responses=ExpenseSerializer),
    update=extend_schema(tags=["finance"], summary="Replace an expense", request=ExpenseSerializer, responses=ExpenseSerializer),
    partial_update=extend_schema(tags=["finance"], summary="Partially update an expense", request=ExpenseSerializer, responses=ExpenseSerializer),
    destroy=extend_schema(tags=["finance"], summary="Delete an expense", responses={204: OpenApiResponse(description="Expense deleted.")}),
)
class ExpenseViewSet(FinancePermissionMixin, viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    search_fields = ["description", "vendor", "reference", "category__name"]
    ordering_fields = ["expense_date", "amount", "created_at"]

    def get_queryset(self):
        queryset = Expense.objects.select_related("category", "created_by")
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category_id=category)
        date_from = self.request.query_params.get("date_from")
        if date_from:
            queryset = queryset.filter(expense_date__gte=date_from)
        date_to = self.request.query_params.get("date_to")
        if date_to:
            queryset = queryset.filter(expense_date__lte=date_to)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema_view(
    list=extend_schema(
        tags=["finance"],
        summary="List payments",
        description="Payment records are immutable after creation.",
        parameters=[
            OpenApiParameter("order", int, OpenApiParameter.QUERY),
            OpenApiParameter("purchase", int, OpenApiParameter.QUERY),
            OpenApiParameter("status", str, OpenApiParameter.QUERY),
            OpenApiParameter("payment_method", str, OpenApiParameter.QUERY),
        ],
        responses=PaymentSerializer(many=True),
    ),
    create=extend_schema(
        tags=["finance"],
        summary="Record a payment",
        description="Record one customer or supplier payment. Exactly one order or purchase is required.",
        request=PaymentSerializer,
        responses={201: PaymentSerializer, 400: OpenApiResponse(description="Invalid or overpaid source document.")},
    ),
    retrieve=extend_schema(tags=["finance"], summary="Retrieve a payment", responses=PaymentSerializer),
)
class PaymentViewSet(
    FinancePermissionMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PaymentSerializer
    search_fields = ["reference", "order__order_number", "purchase__purchase_number"]
    ordering_fields = ["created_at", "paid_at", "amount", "status"]

    def get_queryset(self):
        queryset = Payment.objects.select_related("order", "purchase", "recorded_by")
        for field in ("order", "purchase", "status", "payment_method"):
            value = self.request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{field if field in ("status", "payment_method") else f"{field}_id": value})
        return queryset
