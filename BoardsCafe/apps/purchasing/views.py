from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view

from BoardsCafe.apps.inventory.models import StockBalance
from BoardsCafe.core.permissions import (
    purchasing_create,
    purchasing_delete,
    purchasing_receive,
    purchasing_update,
    purchasing_view,
)
from BoardsCafe.core.throttling import AuthRateThrottle

from .models import Purchase, PurchaseItem, PurchaseReceipt, PurchaseReceiptItem, Supplier
from .serializers import (
    PurchaseReceiptRequestSerializer,
    PurchaseReceiptSerializer,
    PurchaseSerializer,
    PurchaseWriteSerializer,
    SupplierSerializer,
)


class PurchasingPermissionMixin:
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        method = self.request.method
        if method == "POST":
            required_permission = purchasing_create
        elif method in ("PUT", "PATCH"):
            required_permission = purchasing_update
        elif method == "DELETE":
            required_permission = purchasing_delete
        else:
            required_permission = purchasing_view
        return [permissions.IsAuthenticated(), required_permission()]


@extend_schema_view(
    list=extend_schema(tags=["purchasing"], summary="List suppliers", responses=SupplierSerializer(many=True)),
    create=extend_schema(tags=["purchasing"], summary="Create a supplier", request=SupplierSerializer, responses={201: SupplierSerializer}),
    retrieve=extend_schema(tags=["purchasing"], summary="Retrieve a supplier", responses=SupplierSerializer),
    update=extend_schema(tags=["purchasing"], summary="Replace a supplier", request=SupplierSerializer, responses=SupplierSerializer),
    partial_update=extend_schema(tags=["purchasing"], summary="Partially update a supplier", request=SupplierSerializer, responses=SupplierSerializer),
    destroy=extend_schema(tags=["purchasing"], summary="Delete an unused supplier", responses={204: OpenApiResponse(description="Supplier deleted.")}),
)
class SupplierViewSet(PurchasingPermissionMixin, viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    search_fields = ["name", "contact_person", "phone", "email", "tax_id"]
    ordering_fields = ["name", "created_at", "updated_at"]

    def get_queryset(self):
        queryset = Supplier.objects.select_related("created_by")
        supplier_status = self.request.query_params.get("status")
        if supplier_status:
            queryset = queryset.filter(status=supplier_status)
        return queryset

    def get_permissions(self):
        if getattr(self, "action", None) == "deactivate":
            return [permissions.IsAuthenticated(), purchasing_update()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    @extend_schema(
        tags=["purchasing"],
        summary="Deactivate a supplier",
        request=None,
        responses={200: SupplierSerializer, 400: OpenApiResponse(description="The supplier is already inactive.")},
    )
    def deactivate(self, request, pk=None):
        supplier = self.get_object()
        if supplier.status == Supplier.Status.INACTIVE:
            raise ValidationError({"status": "Supplier is already inactive."})
        supplier.status = Supplier.Status.INACTIVE
        supplier.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(supplier).data)


@extend_schema_view(
    list=extend_schema(
        tags=["purchasing"],
        summary="List purchases",
        parameters=[
            OpenApiParameter("supplier", int, OpenApiParameter.QUERY),
            OpenApiParameter("status", str, OpenApiParameter.QUERY),
            OpenApiParameter("date_from", str, OpenApiParameter.QUERY, description="ISO-8601 purchase date."),
            OpenApiParameter("date_to", str, OpenApiParameter.QUERY, description="ISO-8601 purchase date."),
        ],
        responses=PurchaseSerializer(many=True),
    ),
    create=extend_schema(tags=["purchasing"], summary="Create a draft purchase", request=PurchaseWriteSerializer, responses={201: PurchaseSerializer}),
    retrieve=extend_schema(tags=["purchasing"], summary="Retrieve a purchase", responses=PurchaseSerializer),
    update=extend_schema(tags=["purchasing"], summary="Replace a draft purchase", request=PurchaseWriteSerializer, responses=PurchaseSerializer),
    partial_update=extend_schema(tags=["purchasing"], summary="Partially update a draft purchase", request=PurchaseWriteSerializer, responses=PurchaseSerializer),
    destroy=extend_schema(tags=["purchasing"], summary="Delete a draft purchase", responses={204: OpenApiResponse(description="Purchase deleted.")}),
)
class PurchaseViewSet(PurchasingPermissionMixin, viewsets.ModelViewSet):
    search_fields = ["purchase_number", "supplier__name", "supplier_invoice", "notes"]
    ordering_fields = ["purchase_date", "created_at", "status"]

    def get_queryset(self):
        queryset = Purchase.objects.select_related("supplier", "created_by").prefetch_related(
            "items__inventory_item__base_unit", "receipts__items"
        )
        supplier = self.request.query_params.get("supplier")
        if supplier:
            queryset = queryset.filter(supplier_id=supplier)
        purchase_status = self.request.query_params.get("status")
        if purchase_status:
            queryset = queryset.filter(status=purchase_status)
        date_from = self.request.query_params.get("date_from")
        if date_from:
            queryset = queryset.filter(purchase_date__gte=date_from)
        date_to = self.request.query_params.get("date_to")
        if date_to:
            queryset = queryset.filter(purchase_date__lte=date_to)
        return queryset

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PurchaseWriteSerializer
        return PurchaseSerializer

    def get_permissions(self):
        if getattr(self, "action", None) == "submit":
            return [permissions.IsAuthenticated(), purchasing_update()]
        if getattr(self, "action", None) == "receive":
            return [permissions.IsAuthenticated(), purchasing_receive()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        output = PurchaseSerializer(serializer.instance, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        if self.get_object().status != Purchase.Status.DRAFT:
            raise ValidationError("Only draft purchases can be edited.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.status != Purchase.Status.DRAFT:
            raise ValidationError("Only draft purchases can be deleted.")
        instance.delete()

    @action(detail=True, methods=["post"])
    @extend_schema(
        tags=["purchasing"],
        summary="Submit a purchase order",
        description="Moves a complete draft purchase into the ordered state.",
        request=None,
        responses={200: PurchaseSerializer, 400: OpenApiResponse(description="Only complete draft purchases can be submitted.")},
    )
    def submit(self, request, pk=None):
        purchase = self.get_object()
        if purchase.status != Purchase.Status.DRAFT:
            raise ValidationError("Only draft purchases can be submitted.")
        if not purchase.items.exists():
            raise ValidationError("A purchase must contain at least one item.")
        purchase.status = Purchase.Status.ORDERED
        purchase.ordered_at = timezone.now()
        purchase.save(update_fields=["status", "ordered_at", "updated_at"])
        return Response(PurchaseSerializer(purchase, context=self.get_serializer_context()).data)

    @action(detail=True, methods=["post"])
    @extend_schema(
        tags=["purchasing"],
        summary="Receive purchased stock",
        description="Records a receipt, increases stock balances, and advances the purchase receipt status.",
        request=PurchaseReceiptRequestSerializer,
        responses={201: PurchaseReceiptSerializer, 400: OpenApiResponse(description="Invalid receipt data or received quantity.")},
    )
    @transaction.atomic
    def receive(self, request, pk=None):
        purchase = Purchase.objects.select_for_update().get(pk=pk)
        if purchase.status not in (Purchase.Status.ORDERED, Purchase.Status.PARTIALLY_RECEIVED):
            raise ValidationError("Only ordered or partially received purchases can be received.")

        serializer = PurchaseReceiptRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receipt_items = serializer.validated_data["items"]
        item_ids = [item["purchase_item"].pk for item in receipt_items]
        if len(item_ids) != len(set(item_ids)):
            raise ValidationError({"items": "Each purchase item may appear only once per receipt."})

        purchase_items = {
            item.pk: item
            for item in PurchaseItem.objects.select_for_update().filter(
                purchase=purchase,
                pk__in=item_ids,
            ).select_related("inventory_item")
        }
        if len(purchase_items) != len(item_ids):
            raise ValidationError({"items": "Every received item must belong to this purchase."})

        for item_data in receipt_items:
            purchase_item = purchase_items[item_data["purchase_item"].pk]
            remaining = purchase_item.ordered_quantity - purchase_item.received_quantity
            if item_data["quantity_received"] > remaining:
                raise ValidationError({
                    "items": (
                        f"Received quantity for {purchase_item.inventory_item.name} "
                        f"exceeds the remaining ordered quantity ({remaining})."
                    )
                })

        receipt = PurchaseReceipt.objects.create(
            purchase=purchase,
            received_by=request.user,
            notes=serializer.validated_data.get("notes", ""),
        )
        for item_data in receipt_items:
            purchase_item = purchase_items[item_data["purchase_item"].pk]
            quantity = item_data["quantity_received"]
            unit_cost = item_data.get("unit_cost")
            if unit_cost is None:
                unit_cost = purchase_item.unit_cost
            PurchaseReceiptItem.objects.create(
                receipt=receipt,
                purchase_item=purchase_item,
                batch_number=item_data.get("batch_number", ""),
                quantity_received=quantity,
                unit_cost=unit_cost,
                expiry_date=item_data.get("expiry_date"),
            )
            purchase_item.received_quantity += quantity
            purchase_item.save(update_fields=["received_quantity"])

            balance, _ = StockBalance.objects.select_for_update().get_or_create(
                item=purchase_item.inventory_item,
            )
            balance.quantity += quantity
            balance.save(update_fields=["quantity", "updated_at"])

        all_received = not PurchaseItem.objects.filter(
            purchase=purchase,
            received_quantity__lt=F("ordered_quantity"),
        ).exists()
        purchase.status = Purchase.Status.RECEIVED if all_received else Purchase.Status.PARTIALLY_RECEIVED
        if purchase.received_at is None:
            purchase.received_at = timezone.now()
        purchase.save(update_fields=["status", "received_at", "updated_at"])
        return Response(
            PurchaseReceiptSerializer(receipt, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )
