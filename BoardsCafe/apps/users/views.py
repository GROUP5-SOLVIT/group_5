from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import (
    UserSerializer, UserListSerializer,
    UserCreateSerializer, UserUpdateSerializer, PasswordChangeSerializer,
    StaffProfileSerializer, StaffDeactivateSerializer
)
from BoardsCafe.core.permissions import users_view, users_create, users_update, users_deactivate, users_activate
from BoardsCafe.core.throttling import AuthRateThrottle
from BoardsCafe.core.serializers import ActionDetailSerializer

User = get_user_model()


@extend_schema(
    summary="Register new staff member",
    description="Public registration endpoint. Creates a new staff account with email, name, phone, password, and optional role assignment.",
    responses={201: UserSerializer}
)
class RegistrationView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AuthRateThrottle]


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_field = self.username_field
        if attrs.get(username_field):
            attrs[username_field] = attrs[username_field].strip().lower()
        return super().validate(attrs)


@extend_schema(
    summary="Staff login",
    description="Authenticate with email and password. Returns access and refresh JWT tokens.",
    responses={200: {"type": "object", "properties": {"access": {"type": "string"}, "refresh": {"type": "string"}}}}
)
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailTokenObtainPairSerializer
    throttle_classes = [AuthRateThrottle]


@extend_schema(
    summary="Get current user profile",
    description="Returns the authenticated user's profile including role and permissions.",
    responses={200: StaffProfileSerializer}
)
class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = StaffProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    summary="Change password",
    description="Change the authenticated user's password. Requires current password and new password confirmation. Blacklists the current refresh token.",
    request=PasswordChangeSerializer,
    responses={200: ActionDetailSerializer}
)
class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AuthRateThrottle]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        # Blacklist the current refresh token to force re-login
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        return Response({'detail': 'Password changed successfully. Please log in again.'})


@extend_schema(
    summary="List staff members",
    description="List all staff members with pagination, search, and filtering by role/active status.",
    parameters=[
        OpenApiParameter(name='search', type=str, location=OpenApiParameter.QUERY, description='Search by email, first name, or last name'),
        OpenApiParameter(name='role', type=int, location=OpenApiParameter.QUERY, description='Filter by role ID'),
        OpenApiParameter(name='is_active', type=bool, location=OpenApiParameter.QUERY, description='Filter by active status'),
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Page number'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Results per page (max 100)'),
    ],
    responses={200: UserListSerializer}
)
class StaffListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), users_create()]
        return [permissions.IsAuthenticated(), users_view()]

    def get_queryset(self):
        queryset = User.objects.select_related('role').all().order_by('-date_joined')

        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )

        # Filter by role
        role_id = self.request.query_params.get('role')
        if role_id:
            queryset = queryset.filter(role_id=role_id)

        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active_bool = is_active.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(is_active=is_active_bool)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserListSerializer


@extend_schema(
    summary="Retrieve, update, or deactivate staff member",
    description="Retrieve staff details, update staff info/role, or deactivate (with confirmation). Admins only.",
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Staff member ID'),
    ],
    responses={
        200: UserSerializer,
        204: None,
        400: {"type": "object", "properties": {"detail": {"type": "string"}}},
    }
)
class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), users_update()]
        if self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), users_deactivate()]
        return [permissions.IsAuthenticated(), users_view()]

    def get_queryset(self):
        return User.objects.select_related('role').all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Prevent self-deactivation
        if instance == request.user:
            return Response(
                {'detail': 'You cannot deactivate your own account.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent deactivating the last superuser
        if instance.is_superuser:
            superuser_count = User.objects.filter(is_superuser=True, is_active=True).count()
            if superuser_count <= 1:
                return Response(
                    {'detail': 'Cannot deactivate the last active administrator.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = StaffDeactivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Activate staff member",
    description="Activate a previously deactivated staff member.",
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH, description='Staff member ID'),
    ],
    responses={200: {"type": "object", "properties": {"detail": {"type": "string"}}}}
)
class StaffActivateView(generics.GenericAPIView):
    throttle_classes = [AuthRateThrottle]
    serializer_class = ActionDetailSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), users_activate()]

    @extend_schema(request=None, responses={200: ActionDetailSerializer})
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = True
        user.save()
        return Response({'detail': 'User activated successfully.'})


from django.shortcuts import get_object_or_404
