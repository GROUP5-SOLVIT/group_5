from rest_framework import generics, permissions

from BoardsCafe.core.permissions import inventory_view, inventory_create, inventory_update
from BoardsCafe.core.throttling import AuthRateThrottle

from .models import InventoryCategory, InventoryItem, StockBalance, UnitOfMeasure
from .serializers import (
    InventoryCategorySerializer, InventoryItemSerializer, StockBalanceSerializer,
    UnitOfMeasureSerializer,
)


class InventoryPermissionMixin:
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            required_permission = inventory_create
        elif self.request.method in ('PUT', 'PATCH', 'DELETE'):
            required_permission = inventory_update
        else:
            required_permission = inventory_view
        return [permissions.IsAuthenticated(), required_permission()]


class InventoryCategoryListCreateView(InventoryPermissionMixin, generics.ListCreateAPIView):
    serializer_class = InventoryCategorySerializer

    def get_queryset(self):
        queryset = InventoryCategory.objects.all()
        active = self.request.query_params.get('is_active')
        if active is not None:
            queryset = queryset.filter(is_active=active.lower() in ('true', '1', 'yes'))
        return queryset


class InventoryCategoryDetailView(InventoryPermissionMixin, generics.RetrieveUpdateAPIView):
    queryset = InventoryCategory.objects.all()
    serializer_class = InventoryCategorySerializer


class UnitListCreateView(InventoryPermissionMixin, generics.ListCreateAPIView):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer


class UnitDetailView(InventoryPermissionMixin, generics.RetrieveUpdateAPIView):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer


class InventoryItemListCreateView(InventoryPermissionMixin, generics.ListCreateAPIView):
    serializer_class = InventoryItemSerializer

    def get_queryset(self):
        queryset = InventoryItem.objects.select_related('category', 'base_unit', 'stock_balance')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        active = self.request.query_params.get('is_active')
        if active is not None:
            queryset = queryset.filter(is_active=active.lower() in ('true', '1', 'yes'))
        return queryset


class InventoryItemDetailView(InventoryPermissionMixin, generics.RetrieveUpdateAPIView):
    queryset = InventoryItem.objects.select_related('category', 'base_unit', 'stock_balance')
    serializer_class = InventoryItemSerializer


class StockBalanceListView(InventoryPermissionMixin, generics.ListAPIView):
    serializer_class = StockBalanceSerializer

    def get_queryset(self):
        queryset = StockBalance.objects.select_related('item', 'item__base_unit')
        item = self.request.query_params.get('item')
        if item:
            queryset = queryset.filter(item_id=item)
        return queryset


class StockBalanceDetailView(InventoryPermissionMixin, generics.RetrieveAPIView):
    queryset = StockBalance.objects.select_related('item', 'item__base_unit')
    serializer_class = StockBalanceSerializer
