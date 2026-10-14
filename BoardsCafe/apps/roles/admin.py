from django.contrib import admin
from .models import Role, Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('codename', 'name', 'module', 'action')
    list_filter = ('module',)
    search_fields = ('codename', 'name', 'description')
    ordering = ('module', 'action')
    readonly_fields = ('created_at',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    filter_horizontal = ('permissions',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'is_active')}),
        ('Permissions', {'fields': ('permissions',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )