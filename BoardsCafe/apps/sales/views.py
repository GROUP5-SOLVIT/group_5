
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from .models import Order
from .serializers import OrderReceiptSerializer, OrderSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["sales"],
        summary="List orders",
        description="Returns orders accessible to the authenticated user. Staff users can view all orders.",
        responses={200: OrderSerializer(many=True)},
    ),
    create=extend_schema(
        tags=["sales"],
        summary="Create an order",
        description="Creates a new draft order using the supplied order data.",
        request=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: OpenApiResponse(description="Invalid order data."),
        },
    ),
    retrieve=extend_schema(
        tags=["sales"],
        summary="Retrieve an order",
        responses={
            200: OrderSerializer,
            404: OpenApiResponse(description="Order not found."),
        },
    ),
    update=extend_schema(
        tags=["sales"],
        summary="Update an order",
        description="Updates an order. Only draft orders can be edited.",
        request=OrderSerializer,
        responses={200: OrderSerializer, 400: OpenApiResponse(description="Invalid data or order is not a draft.")},
    ),
    partial_update=extend_schema(
        tags=["sales"],
        summary="Partially update an order",
        description="Updates selected fields of a draft order.",
        request=OrderSerializer,
        responses={200: OrderSerializer, 400: OpenApiResponse(description="Invalid data or order is not a draft.")},
    ),
    destroy=extend_schema(
        tags=["sales"],
        summary="Delete an order",
        description="Deletes an order only if its status is draft.",
        responses={
            204: OpenApiResponse(description="Order deleted successfully."),
            400: OpenApiResponse(description="Only draft orders can be deleted."),
        },
    ),
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["order_number", "notes"]
    ordering_fields = ["created_at", "total_amount", "status"]
    filterset_fields = ["status"]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("items")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(created_by=self.request.user)

    def perform_update(self, serializer):
        order = self.get_object()
        if order.status != Order.Status.DRAFT:
            raise ValidationError("Only draft orders can be edited.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.status != Order.Status.DRAFT:
            raise ValidationError("Only draft orders can be deleted.")
        instance.delete()

    @action(detail=True, methods=["post"])
    @extend_schema(
        tags=["sales"],
        summary="Submit an order",
        description="Submits a draft order for payment after validating its items and total.",
        request=None,
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="The order cannot be submitted in its current state."),
        },
    )
    @transaction.atomic
    def submit(self, request, pk=None):
        order = self.get_object()

        if order.status != Order.Status.DRAFT:
            raise ValidationError("Only draft orders can be submitted.")
        if not order.items.exists():
            raise ValidationError("An order must contain at least one item.")
        if order.total_amount <= 0:
            raise ValidationError("Order total must be greater than zero.")

        order.status = Order.Status.PENDING
        order.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(order).data)

    @action(detail=True, methods=["get"])
    @extend_schema(
        tags=["sales"],
        summary="Get an order receipt",
        description="Returns a receipt for a paid or refunded order.",
        responses={
            200: OrderReceiptSerializer,
            400: OpenApiResponse(description="A receipt is available only after a completed sale."),
        },
    )
    def receipt(self, request, pk=None):
        order = self.get_object()
        if order.status not in [Order.Status.PAID, Order.Status.REFUNDED]:
            raise ValidationError(
                "A receipt is available only after a completed sale."
            )

        return Response({
            "order_number": str(order.order_number),
            "status": order.status,
            "created_at": order.created_at,
            "items": [
                {
                    "product": item.product_name,
                    "variant": item.variant_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "line_total": item.line_total,
                }
                for item in order.items.all()
            ],
            "subtotal": order.subtotal,
            "discount": order.discount_amount,
            "tax": order.tax_amount,
            "total": order.total_amount,
        })
