from rest_framework import generics, permissions, viewsets
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view

from BoardsCafe.core.permissions import (
    recipes_create,
    recipes_delete,
    recipes_update,
    recipes_view,
)
from BoardsCafe.core.throttling import AuthRateThrottle

from .models import Recipe, RecipeIngredient
from .serializers import RecipeIngredientSerializer, RecipeSerializer


class RecipePermissionMixin:
    """Apply the recipe RBAC policy consistently to recipes and ingredients."""

    throttle_classes = [AuthRateThrottle]

    def get_permissions(self):
        method = self.request.method
        if method == "POST":
            required_permission = recipes_create
        elif method in ("PUT", "PATCH"):
            required_permission = recipes_update
        elif method == "DELETE":
            required_permission = recipes_delete
        else:
            required_permission = recipes_view
        return [permissions.IsAuthenticated(), required_permission()]


@extend_schema_view(
    list=extend_schema(
        tags=["recipes"],
        summary="List recipes",
        parameters=[
            OpenApiParameter("product", int, OpenApiParameter.QUERY, description="Filter by menu product ID."),
            OpenApiParameter("is_active", bool, OpenApiParameter.QUERY, description="Filter by active status."),
        ],
        responses=RecipeSerializer(many=True),
    ),
    create=extend_schema(
        tags=["recipes"],
        summary="Create a recipe",
        request=RecipeSerializer,
        responses={201: RecipeSerializer, 400: OpenApiResponse(description="Invalid recipe data.")},
    ),
    retrieve=extend_schema(tags=["recipes"], summary="Retrieve a recipe", responses=RecipeSerializer),
    update=extend_schema(tags=["recipes"], summary="Replace a recipe", request=RecipeSerializer, responses=RecipeSerializer),
    partial_update=extend_schema(tags=["recipes"], summary="Partially update a recipe", request=RecipeSerializer, responses=RecipeSerializer),
    destroy=extend_schema(tags=["recipes"], summary="Delete a recipe", responses={204: OpenApiResponse(description="Recipe deleted.")}),
)
class RecipeViewSet(RecipePermissionMixin, viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    search_fields = ["name", "product__name", "instructions"]
    ordering_fields = ["name", "created_at", "updated_at"]

    def get_queryset(self):
        queryset = Recipe.objects.select_related("product", "created_by").prefetch_related(
            "ingredients__inventory_item__base_unit"
        )
        product_id = self.request.query_params.get("product")
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() in ("true", "1", "yes"))
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(
    tags=["recipes"],
    summary="List or add recipe ingredients",
    parameters=[
        OpenApiParameter("recipe_pk", int, OpenApiParameter.PATH, description="Recipe ID."),
    ],
    responses={200: RecipeIngredientSerializer(many=True), 201: RecipeIngredientSerializer},
)
class RecipeIngredientListCreateView(RecipePermissionMixin, generics.ListCreateAPIView):
    serializer_class = RecipeIngredientSerializer

    def get_queryset(self):
        return RecipeIngredient.objects.filter(recipe_id=self.kwargs["recipe_pk"]).select_related(
            "recipe", "inventory_item", "inventory_item__base_unit"
        )

    def perform_create(self, serializer):
        recipe = generics.get_object_or_404(Recipe, pk=self.kwargs["recipe_pk"])
        serializer.save(recipe=recipe)


@extend_schema(
    tags=["recipes"],
    summary="Retrieve, update, or remove a recipe ingredient",
    parameters=[
        OpenApiParameter("recipe_pk", int, OpenApiParameter.PATH, description="Recipe ID."),
        OpenApiParameter("pk", int, OpenApiParameter.PATH, description="Ingredient ID."),
    ],
    responses={200: RecipeIngredientSerializer, 204: OpenApiResponse(description="Ingredient removed.")},
)
class RecipeIngredientDetailView(RecipePermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeIngredientSerializer

    def get_queryset(self):
        return RecipeIngredient.objects.filter(recipe_id=self.kwargs["recipe_pk"]).select_related(
            "recipe", "inventory_item", "inventory_item__base_unit"
        )
