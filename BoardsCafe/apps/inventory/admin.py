from django.contrib import admin

from .models import InventoryCategory, InventoryItem, StockBalance, UnitOfMeasure


@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'updated_at')
    search_fields = ('name', 'symbol')


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'base_unit', 'minimum_stock_level', 'is_active')
    search_fields = ('name', 'sku')
    list_filter = ('category', 'is_active')


@admin.register(StockBalance)
class StockBalanceAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'updated_at')
    readonly_fields = ('item', 'quantity', 'created_at', 'updated_at')
