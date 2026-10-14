from django.urls import path
from .views import (
    PermissionListView,
    RoleListCreateView, RoleDetailView,
    RolePermissionsView, RoleDeactivateView, RoleActivateView
)

app_name = 'roles'

urlpatterns = [
    # Permissions
    path('permissions/', PermissionListView.as_view(), name='permission-list'),

    # Roles
    path('', RoleListCreateView.as_view(), name='role-list-create'),
    path('<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('<int:pk>/permissions/', RolePermissionsView.as_view(), name='role-permissions'),
    path('<int:pk>/deactivate/', RoleDeactivateView.as_view(), name='role-deactivate'),
    path('<int:pk>/activate/', RoleActivateView.as_view(), name='role-activate'),
]