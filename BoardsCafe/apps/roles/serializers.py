from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Role, Permission


class PermissionSerializer(serializers.ModelSerializer):
    full_codename = serializers.CharField(read_only=True)

    class Meta:
        model = Permission
        fields = ('id', 'codename', 'name', 'module', 'action', 'description', 'full_codename', 'created_at')
        read_only_fields = ('id', 'created_at', 'full_codename')


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        source='permissions',
        write_only=True,
        many=True,
        required=False
    )
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = (
            'id', 'name', 'description', 'permissions', 'permission_ids',
            'is_active', 'users_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'users_count')

    @extend_schema_field(serializers.IntegerField())
    def get_users_count(self, obj):
        return obj.users.count()


class RoleCreateSerializer(serializers.ModelSerializer):
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        source='permissions',
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'permission_ids', 'is_active')
        read_only_fields = ('id',)

    def validate_name(self, value):
        if Role.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('A role with this name already exists.')
        return value


class RoleUpdateSerializer(serializers.ModelSerializer):
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        source='permissions',
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'permission_ids', 'is_active')
        read_only_fields = ('id',)

    def validate_name(self, value):
        if Role.objects.exclude(pk=self.instance.pk).filter(name__iexact=value).exists():
            raise serializers.ValidationError('A role with this name already exists.')
        return value


class PermissionListSerializer(serializers.ModelSerializer):
    full_codename = serializers.CharField(read_only=True)

    class Meta:
        model = Permission
        fields = ('id', 'codename', 'name', 'module', 'action', 'description', 'full_codename', 'created_at')
        read_only_fields = fields


class RolePermissionIdsSerializer(serializers.Serializer):
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        default=list,
    )
