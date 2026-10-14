from django.contrib import admin
from .models import BusinessProfile, Floor, Table, PaymentMethod, BusinessConfiguration


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'email', 'phone', 'currency', 'timezone', 'is_active', 'created_at')
    list_filter = ('is_active', 'currency', 'timezone')
    search_fields = ('name', 'category', 'email', 'phone', 'tin', 'address')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    fieldsets = (
        (None, {'fields': ('name', 'category', 'is_active')}),
        ('Contact', {'fields': ('email', 'phone', 'address')}),
        ('Business Details', {'fields': ('tin', 'currency', 'timezone', 'logo')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'created_by')}),
    )


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'display_order', 'is_active', 'created_at')
    list_filter = ('is_active', 'business')
    search_fields = ('name', 'description', 'business__name')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    fieldsets = (
        (None, {'fields': ('business', 'name', 'description', 'display_order', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'created_by')}),
    )


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor', 'name', 'capacity', 'status', 'is_active', 'created_at')
    list_filter = ('status', 'is_active', 'floor__business', 'floor')
    search_fields = ('number', 'name', 'floor__name', 'floor__business__name')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    fieldsets = (
        (None, {'fields': ('floor', 'number', 'name', 'capacity', 'status', 'is_active')}),
        ('Position', {'fields': ('position_x', 'position_y')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'created_by')}),
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_type', 'is_active', 'is_default', 'display_order', 'requires_reference')
    list_filter = ('is_active', 'payment_type', 'is_default', 'requires_reference')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    fieldsets = (
        (None, {'fields': ('name', 'payment_type', 'description', 'is_active', 'is_default', 'display_order', 'requires_reference')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'created_by')}),
    )


@admin.register(BusinessConfiguration)
class BusinessConfigurationAdmin(admin.ModelAdmin):
    list_display = ('business', 'default_payment_method', 'low_stock_threshold', 'expiry_warning_days', 'tax_rate', 'service_charge_rate')
    search_fields = ('business__name',)
    readonly_fields = ('created_at', 'updated_at', 'updated_by')
    fieldsets = (
        (None, {'fields': ('business',)}),
        ('Receipt', {'fields': ('receipt_footer', 'default_payment_method')}),
        ('Inventory', {'fields': ('low_stock_threshold', 'expiry_warning_days')}),
        ('Features', {'fields': ('enable_table_service', 'enable_takeaway', 'enable_delivery')}),
        ('Financial', {'fields': ('tax_rate', 'service_charge_rate')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'updated_by')}),
    )