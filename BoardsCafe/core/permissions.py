from rest_framework.permissions import BasePermission


class BaseHasPermission(BasePermission):
    """Base permission class that checks if user has required permissions."""
    message = 'You do not have permission to perform this action.'
    required_permissions = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        user_permissions = getattr(request.user, 'get_all_permissions', lambda: set())()

        # If no required permissions specified, allow any authenticated user
        if not self.required_permissions:
            return True

        # Check if user has all required permissions
        return all(perm in user_permissions for perm in self.required_permissions)


class IsAdminUser(BasePermission):
    message = 'Administrator access required.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


# Permission classes for specific permissions - these are CLASSES, not instances
# DRF will instantiate them when processing permission_classes
def permission_class(permission):
    """Factory function to create a permission class for a specific permission."""
    class SpecificPermission(BaseHasPermission):
        required_permissions = [permission]
    return SpecificPermission


settings_view = permission_class('settings.view')
settings_update = permission_class('settings.update')
inventory_view = permission_class('inventory.view')
inventory_create = permission_class('inventory.create')
inventory_update = permission_class('inventory.update')
users_view = permission_class('users.view')
users_create = permission_class('users.create')
users_update = permission_class('users.update')
users_deactivate = permission_class('users.deactivate')
users_activate = permission_class('users.activate')
roles_view = permission_class('roles.view')
roles_create = permission_class('roles.create')
roles_update = permission_class('roles.update')
roles_delete = permission_class('roles.delete')
roles_assign = permission_class('roles.assign_permissions')
permissions_view = permission_class('permissions.view')

# Recipe permissions
recipes_view = permission_class('recipes.view')
recipes_create = permission_class('recipes.create')
recipes_update = permission_class('recipes.update')
recipes_delete = permission_class('recipes.delete')

# Purchasing permissions
purchasing_view = permission_class('purchasing.view')
purchasing_create = permission_class('purchasing.create')
purchasing_update = permission_class('purchasing.update')
purchasing_receive = permission_class('purchasing.receive')
purchasing_delete = permission_class('purchasing.delete')

# Finance permissions
finance_view = permission_class('finance.view')
finance_create = permission_class('finance.create')
finance_update = permission_class('finance.update')
finance_delete = permission_class('finance.delete')

# Read-only analytical endpoints
dashboard_view = permission_class('dashboard.view')
reports_view = permission_class('reports.view')


# Convenience function to check if user has a specific permission
def user_has_permission(user, permission_codename):
    """Check if a user has a specific permission by codename."""
    permissions = user.get_all_permissions()
    return permission_codename in permissions
