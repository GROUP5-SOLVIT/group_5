from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import BusinessProfile, Floor, Table, PaymentMethod, BusinessConfiguration
from .serializers import (
    BusinessProfileSerializer, BusinessProfileCreateSerializer,
    FloorSerializer, FloorCreateSerializer,
    TableSerializer, TableCreateSerializer,
    PaymentMethodSerializer, PaymentMethodCreateSerializer,
    BusinessConfigurationSerializer, BusinessConfigurationUpdateSerializer
)
from BoardsCafe.core.permissions import settings_view, settings_update
from BoardsCafe.core.throttling import AuthRateThrottle


@extend_schema(
    summary="List and create business profiles",
    description="List all business profiles or create a new one. Only one profile can be active at a time.",
    parameters=[
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Results per page (max 100)'),
    ],
    responses={200: BusinessProfileSerializer, 201: BusinessProfileSerializer}
)
class BusinessProfileListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_queryset(self):
        return BusinessProfile.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BusinessProfileCreateSerializer
        return BusinessProfileSerializer


@extend_schema(
    summary="Retrieve, update, or deactivate business profile",
    description="Retrieve business profile details, update profile info, or deactivate (sets is_active=False).",
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Business profile ID'),
    ],
    responses={
        200: BusinessProfileSerializer,
        204: None,
    }
)
class BusinessProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AuthRateThrottle]
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_queryset(self):
        return BusinessProfile.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BusinessProfileCreateSerializer
        return BusinessProfileSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="List and create floors for a business",
    description="List all floors for a business or create a new floor.",
    parameters=[
        OpenApiParameter(name='business_pk', type=int, location=OpenApiParameter.PATH, description='Business profile ID'),
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Results per page (max 100)'),
    ],
    responses={200: FloorSerializer, 201: FloorSerializer}
)
class FloorListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_queryset(self):
        business_id = self.kwargs.get('business_pk')
        return Floor.objects.filter(business_id=business_id).order_by('display_order', 'name')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FloorCreateSerializer
        return FloorSerializer

    def perform_create(self, serializer):
        business = get_object_or_404(BusinessProfile, pk=self.kwargs['business_pk'])
        serializer.save(business=business, created_by=self.request.user)


@extend_schema(
    summary="Retrieve, update, or deactivate floor",
    description="Retrieve floor details, update floor info, or deactivate (sets is_active=False).",
    parameters=[
        OpenApiParameter(name='business_pk', type=int, location=OpenApiParameter.PATH, description='Business profile ID'),
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Floor ID'),
    ],
    responses={
        200: FloorSerializer,
        204: None,
    }
)
class FloorDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AuthRateThrottle]
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_queryset(self):
        business_id = self.kwargs.get('business_pk')
        return Floor.objects.filter(business_id=business_id)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return FloorCreateSerializer
        return FloorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="List and create tables for a floor",
    description="List all tables for a floor or create a new table.",
    parameters=[
        OpenApiParameter(name='business_pk', type=int, location=OpenApiParameter.PATH, description='Business profile ID'),
        OpenApiParameter(name='floor_pk', type=int, location=OpenApiParameter.PATH, description='Floor ID'),
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Results per page (max 100)'),
    ],
    responses={200: TableSerializer, 201: TableSerializer}
)
class TableListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_queryset(self):
        floor_id = self.kwargs.get('floor_pk')
        return Table.objects.filter(floor_id=floor_id).order_by('number')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TableCreateSerializer
        return TableSerializer

    def perform_create(self, serializer):
        floor = get_object_or_404(Floor, pk=self.kwargs['floor_pk'])
        serializer.save(floor=floor, created_by=self.request.user)


@extend_schema(
    summary="Retrieve, update, or deactivate table",
    description="Retrieve table details, update table info/status, or deactivate (sets is_active=False).",
    parameters=[
        OpenApiParameter(name='business_pk', type=int, location=OpenApiParameter.PATH, description='Business profile ID'),
        OpenApiParameter(name='floor_pk', type=int, location=OpenApiParameter.PATH, description='Floor ID'),
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Table ID'),
    ],
    responses={
        200: TableSerializer,
        204: None,
    }
)
class TableDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AuthRateThrottle]
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_queryset(self):
        floor_id = self.kwargs.get('floor_pk')
        return Table.objects.filter(floor_id=floor_id)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TableCreateSerializer
        return TableSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="List and create payment methods",
    description="List all payment methods or create a new one.",
    parameters=[
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Results per page (max 100)'),
    ],
    responses={200: PaymentMethodSerializer, 201: PaymentMethodSerializer}
)
class PaymentMethodListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_queryset(self):
        return PaymentMethod.objects.all().order_by('display_order', 'name')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentMethodCreateSerializer
        return PaymentMethodSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(
    summary="Retrieve, update, or deactivate payment method",
    description="Retrieve payment method details, update info, or deactivate (sets is_active=False).",
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Payment method ID'),
    ],
    responses={
        200: PaymentMethodSerializer,
        204: None,
    }
)
class PaymentMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AuthRateThrottle]
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_queryset(self):
        return PaymentMethod.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PaymentMethodCreateSerializer
        return PaymentMethodSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Retrieve or update business configuration",
    description="Retrieve or update business configuration settings (tax, service charge, features, etc.).",
    parameters=[
        OpenApiParameter(name='business_pk', type=int, location=OpenApiParameter.PATH, description='Business profile ID'),
    ],
    responses={200: BusinessConfigurationSerializer}
)
class BusinessConfigurationDetailView(generics.RetrieveUpdateAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), settings_update()]
        return [permissions.IsAuthenticated(), settings_view()]

    def get_object(self):
        business_id = self.kwargs.get('business_pk')
        business = get_object_or_404(BusinessProfile, pk=business_id)
        config, created = BusinessConfiguration.objects.get_or_create(business=business)
        return config

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BusinessConfigurationUpdateSerializer
        return BusinessConfigurationSerializer


@extend_schema(
    summary="Get default configuration values",
    description="Returns default configuration values for payment types, table statuses, currency, and timezone.",
    responses={200: {"type": "object", "properties": {
        "payment_types": {"type": "array", "items": {"type": "object"}},
        "table_statuses": {"type": "array", "items": {"type": "object"}},
        "default_currency": {"type": "string"},
        "default_timezone": {"type": "string"},
    }}}
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, settings_view])
def business_config_defaults(request):
    """Get default configuration values for reference."""
    return Response({
        'payment_types': [
            {'value': 'CASH', 'label': 'Cash'},
            {'value': 'MOBILE_MONEY', 'label': 'Mobile Money'},
            {'value': 'CARD', 'label': 'Card'},
            {'value': 'BANK_TRANSFER', 'label': 'Bank Transfer'},
            {'value': 'CHEQUE', 'label': 'Cheque'},
            {'value': 'CUSTOMER_CREDIT', 'label': 'Customer Credit'},
        ],
        'table_statuses': [
            {'value': 'AVAILABLE', 'label': 'Available'},
            {'value': 'OCCUPIED', 'label': 'Occupied'},
            {'value': 'RESERVED', 'label': 'Reserved'},
            {'value': 'MAINTENANCE', 'label': 'Maintenance'},
        ],
        'default_currency': 'RWF',
        'default_timezone': 'Africa/Kigali',
    })
