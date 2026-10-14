from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import BusinessProfile, Floor, Table, PaymentMethod, BusinessConfiguration


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = (
            'id', 'name', 'category', 'email', 'phone', 'address', 'tin',
            'currency', 'timezone', 'logo', 'is_active', 'created_at', 'updated_at', 'created_by'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')


class BusinessProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = (
            'id', 'name', 'category', 'email', 'phone', 'address', 'tin',
            'currency', 'timezone', 'logo'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FloorSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)
    tables_count = serializers.SerializerMethodField()

    class Meta:
        model = Floor
        fields = (
            'id', 'business', 'business_name', 'name', 'description',
            'display_order', 'is_active', 'tables_count', 'created_at', 'updated_at', 'created_by'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')

    @extend_schema_field(serializers.IntegerField())
    def get_tables_count(self, obj):
        return obj.tables.filter(is_active=True).count()


class FloorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ('id', 'business', 'name', 'description', 'display_order', 'is_active')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TableSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    business_name = serializers.CharField(source='floor.business.name', read_only=True)

    class Meta:
        model = Table
        fields = (
            'id', 'floor', 'floor_name', 'business_name', 'number', 'name',
            'capacity', 'status', 'position_x', 'position_y', 'is_active',
            'created_at', 'updated_at', 'created_by'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')


class TableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'floor', 'number', 'name', 'capacity', 'status', 'position_x', 'position_y', 'is_active')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = (
            'id', 'name', 'payment_type', 'description', 'is_active',
            'is_default', 'display_order', 'requires_reference',
            'created_at', 'updated_at', 'created_by'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')


class PaymentMethodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = (
            'id', 'name', 'payment_type', 'description', 'is_active',
            'is_default', 'display_order', 'requires_reference'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class BusinessConfigurationSerializer(serializers.ModelSerializer):
    default_payment_method_detail = PaymentMethodSerializer(source='default_payment_method', read_only=True)

    class Meta:
        model = BusinessConfiguration
        fields = (
            'id', 'business', 'receipt_footer', 'default_payment_method',
            'default_payment_method_detail', 'low_stock_threshold',
            'expiry_warning_days', 'enable_table_service', 'enable_takeaway',
            'enable_delivery', 'tax_rate', 'service_charge_rate',
            'created_at', 'updated_at', 'updated_by'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'updated_by')


class BusinessConfigurationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessConfiguration
        fields = (
            'receipt_footer', 'default_payment_method', 'low_stock_threshold',
            'expiry_warning_days', 'enable_table_service', 'enable_takeaway',
            'enable_delivery', 'tax_rate', 'service_charge_rate'
        )

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)