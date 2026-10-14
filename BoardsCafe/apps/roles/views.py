from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Role, Permission
from .serializers import (
    RoleSerializer, RoleCreateSerializer, RoleUpdateSerializer,
    PermissionSerializer, PermissionListSerializer,
    RolePermissionIdsSerializer,
)
from BoardsCafe.core.permissions import roles_view, roles_create, roles_update, roles_delete, roles_assign, permissions_view
from BoardsCafe.core.throttling import AuthRateThrottle
from BoardsCafe.core.serializers import ActionDetailSerializer


@extend_schema(
    summary="List all permissions",
    description="List all available permissions grouped by module and action.",
    parameters=[
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Results per page (max 100)'),
    ],
    responses={200: PermissionListSerializer}
)
class PermissionListView(generics.ListAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        return [permissions.IsAuthenticated(), permissions_view()]

    queryset = Permission.objects.all().order_by('module', 'action', 'codename')
    serializer_class = PermissionListSerializer


@extend_schema(
    summary="List and create roles",
    description="List all roles with permissions, or create a new role with permission assignments.",
    parameters=[
        OpenApiParameter(name='search', type=str, location=OpenApiParameter.QUERY, description='Search by role name or description'),
        OpenApiParameter(name='is_active', type=bool, location=OpenApiParameter.QUERY, description='Filter by active status'),
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Results per page (max 100)'),
    ],
    responses={200: RoleSerializer, 201: RoleSerializer}
)
class RoleListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), roles_create()]
        return [permissions.IsAuthenticated(), roles_view()]

    def get_queryset(self):
        queryset = Role.objects.prefetch_related('permissions').all().order_by('name')

        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )

        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active_bool = is_active.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(is_active=is_active_bool)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoleCreateSerializer
        return RoleSerializer


@extend_schema(
    summary="Retrieve, update, or delete role",
    description="Retrieve role details with permissions, update role info/permissions, or delete (with safeguards).",
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Role ID'),
    ],
    responses={
        200: RoleSerializer,
        204: None,
        400: {"type": "object", "properties": {"detail": {"type": "string"}}},
    }
)
class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AuthRateThrottle]
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), roles_update()]
        if self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), roles_delete()]
        return [permissions.IsAuthenticated(), roles_view()]

    def get_queryset(self):
        return Role.objects.prefetch_related('permissions').all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RoleUpdateSerializer
        return RoleSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Prevent deletion if role has users assigned
        if instance.users.exists():
            return Response(
                {'detail': 'Cannot delete role with assigned users. Deactivate instead.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent deletion of system roles
        if instance.name in ['Administrator', 'Manager']:
            return Response(
                {'detail': 'Cannot delete system roles.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Manage role permissions",
    description="Get, assign, or remove permissions for a role.",
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Role ID'),
    ],
)
class RolePermissionsView(generics.GenericAPIView):
    throttle_classes = [AuthRateThrottle]
    serializer_class = RolePermissionIdsSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), roles_assign()]

    @extend_schema(
        request=None,
        responses=PermissionSerializer(many=True),
        operation_id='role_assigned_permissions_list',
    )
    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        permissions = role.permissions.all().order_by('module', 'action', 'codename')
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

    @extend_schema(request=RolePermissionIdsSerializer, responses={200: ActionDetailSerializer, 400: ActionDetailSerializer})
    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        permission_ids = request.data.get('permission_ids', [])

        if not isinstance(permission_ids, list):
            return Response(
                {'detail': 'permission_ids must be a list.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        permissions = Permission.objects.filter(id__in=permission_ids)
        role.permissions.add(*permissions)
        return Response({'detail': 'Permissions assigned successfully.'})

    @extend_schema(request=RolePermissionIdsSerializer, responses={200: ActionDetailSerializer, 400: ActionDetailSerializer})
    def delete(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        permission_ids = request.data.get('permission_ids', [])

        if not isinstance(permission_ids, list):
            return Response(
                {'detail': 'permission_ids must be a list.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        permissions = Permission.objects.filter(id__in=permission_ids)
        role.permissions.remove(*permissions)
        return Response({'detail': 'Permissions removed successfully.'})


@extend_schema(
    summary="Deactivate role",
    description="Deactivate a role (sets is_active=False). Cannot deactivate system roles (Administrator, Manager) or roles with active users.",
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Role ID'),
    ],
    responses={200: ActionDetailSerializer}
)
class RoleDeactivateView(generics.GenericAPIView):
    throttle_classes = [AuthRateThrottle]
    serializer_class = ActionDetailSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), roles_update()]

    @extend_schema(request=None, responses={200: ActionDetailSerializer})
    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)

        # Prevent deactivating system roles
        if role.name in ['Administrator', 'Manager']:
            return Response(
                {'detail': 'Cannot deactivate system roles.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if role has active users
        if role.users.filter(is_active=True).exists():
            return Response(
                {'detail': 'Cannot deactivate role with active users. Reassign users first.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        role.is_active = False
        role.save()
        return Response({'detail': 'Role deactivated successfully.'})


@extend_schema(
    summary="Activate role",
    description="Activate a previously deactivated role.",
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Role ID'),
    ],
    responses={200: ActionDetailSerializer}
)
class RoleActivateView(generics.GenericAPIView):
    throttle_classes = [AuthRateThrottle]
    serializer_class = ActionDetailSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), roles_update()]

    @extend_schema(request=None, responses={200: ActionDetailSerializer})
    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        role.is_active = True
        role.save()
        return Response({'detail': 'Role activated successfully.'})
