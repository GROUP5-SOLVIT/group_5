from django.urls import path

from .views import (
    InventoryCategoryDetailView, InventoryCategoryListCreateView,
    InventoryItemDetailView, InventoryItemListCreateView, StockBalanceDetailView,
    StockBalanceListView, UnitDetailView, UnitListCreateView,
)

app_name = 'inventory'

urlpatterns = [
    path('categories/', InventoryCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', InventoryCategoryDetailView.as_view(), name='category-detail'),
    path('units/', UnitListCreateView.as_view(), name='unit-list-create'),
    path('units/<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('items/', InventoryItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', InventoryItemDetailView.as_view(), name='item-detail'),
    path('stock-balances/', StockBalanceListView.as_view(), name='stock-balance-list'),
    path('stock-balances/<int:pk>/', StockBalanceDetailView.as_view(), name='stock-balance-detail'),
]
