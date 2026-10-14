
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from .models import Category, Product, ProductVariant
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductVariantSerializer,
)


class MenuPermissionMixin:
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Only staff users can manage the menu."
            )
        serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Only staff users can manage the menu."
            )
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Only staff users can manage the menu."
            )
        instance.delete()


@extend_schema_view(
    list=extend_schema(
        tags=["menu"],
        summary="List menu categories",
        description="Lists menu categories. This endpoint is publicly accessible.",
    ),
    create=extend_schema(
        tags=["menu"],
        summary="Create a menu category",
        description="Creates a category. Only authenticated staff can manage menu data.",
        responses={
            201: CategorySerializer,
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    retrieve=extend_schema(
        tags=["menu"],
        summary="Retrieve a menu category",
        description="Returns a category and its details. This endpoint is publicly accessible.",
    ),
    update=extend_schema(
        tags=["menu"],
        summary="Update a menu category",
        description="Updates a category. Only authenticated staff can manage menu data.",
        responses={
            200: CategorySerializer,
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    partial_update=extend_schema(
        tags=["menu"],
        summary="Partially update a menu category",
        description="Updates selected category fields. Only authenticated staff can manage menu data.",
        responses={
            200: CategorySerializer,
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    destroy=extend_schema(
        tags=["menu"],
        summary="Delete a menu category",
        description="Deletes a category. Only authenticated staff can manage menu data.",
        responses={
            204: OpenApiResponse(description="Category deleted successfully."),
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
)
class CategoryViewSet(MenuPermissionMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    filterset_fields = ["is_active"]


@extend_schema_view(
    list=extend_schema(
        tags=["menu"],
        summary="List menu products",
        description="Lists products with category and variant details. This endpoint is publicly accessible.",
    ),
    create=extend_schema(
        tags=["menu"],
        summary="Create a menu product",
        description="Creates a product. Only authenticated staff can manage menu data.",
        responses={
            201: ProductSerializer,
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    retrieve=extend_schema(
        tags=["menu"],
        summary="Retrieve a menu product",
        description="Returns product details, including its category and variants. This endpoint is publicly accessible.",
    ),
    update=extend_schema(
        tags=["menu"],
        summary="Update a menu product",
        description="Updates a product. Only authenticated staff can manage menu data.",
        responses={
            200: ProductSerializer,
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    partial_update=extend_schema(
        tags=["menu"],
        summary="Partially update a menu product",
        description="Updates selected product fields. Only authenticated staff can manage menu data.",
        responses={
            200: ProductSerializer,
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    destroy=extend_schema(
        tags=["menu"],
        summary="Delete a menu product",
        description="Deletes a product. Only authenticated staff can manage menu data.",
        responses={
            204: OpenApiResponse(description="Product deleted successfully."),
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
)
class ProductViewSet(MenuPermissionMixin, viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related(
        "variants"
    )
    serializer_class = ProductSerializer
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["name", "base_price", "created_at"]
    filterset_fields = ["category", "is_available"]


@extend_schema_view(
    list=extend_schema(
        tags=["menu"],
        summary="List product variants",
        description="Lists variants and their product information. This endpoint is publicly accessible.",
    ),
    create=extend_schema(
        tags=["menu"],
        summary="Create a product variant",
        description="Creates a variant with a non-negative effective product price. Only authenticated staff can manage menu data.",
        responses={
            201: ProductVariantSerializer,
            400: OpenApiResponse(description="Invalid variant data."),
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    retrieve=extend_schema(
        tags=["menu"],
        summary="Retrieve a product variant",
        description="Returns variant details. This endpoint is publicly accessible.",
    ),
    update=extend_schema(
        tags=["menu"],
        summary="Update a product variant",
        description="Updates a variant. Only authenticated staff can manage menu data.",
        responses={
            200: ProductVariantSerializer,
            400: OpenApiResponse(description="Invalid variant data."),
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    partial_update=extend_schema(
        tags=["menu"],
        summary="Partially update a product variant",
        description="Updates selected variant fields. Only authenticated staff can manage menu data.",
        responses={
            200: ProductVariantSerializer,
            400: OpenApiResponse(description="Invalid variant data."),
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
    destroy=extend_schema(
        tags=["menu"],
        summary="Delete a product variant",
        description="Deletes a variant. Only authenticated staff can manage menu data.",
        responses={
            204: OpenApiResponse(description="Variant deleted successfully."),
            403: OpenApiResponse(description="Only staff users can manage the menu."),
        },
    ),
)
class ProductVariantViewSet(
    MenuPermissionMixin, viewsets.ModelViewSet
):
    queryset = ProductVariant.objects.select_related("product")
    serializer_class = ProductVariantSerializer
    search_fields = ["name", "product__name"]
    ordering_fields = ["name", "price_adjustment", "created_at"]
    filterset_fields = ["product", "is_available"]
