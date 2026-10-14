from rest_framework import serializers

from BoardsCafe.apps.inventory.models import InventoryItem
from BoardsCafe.apps.menu.models import Product

from .models import Recipe, RecipeIngredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    inventory_item_name = serializers.CharField(
        source="inventory_item.name",
        read_only=True,
    )
    unit = serializers.IntegerField(
        source="inventory_item.base_unit_id",
        read_only=True,
    )
    unit_name = serializers.CharField(
        source="inventory_item.base_unit.name",
        read_only=True,
    )
    unit_symbol = serializers.CharField(
        source="inventory_item.base_unit.symbol",
        read_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            "id", "recipe", "inventory_item", "inventory_item_name",
            "unit", "unit_name", "unit_symbol", "quantity_required",
            "notes", "created_at", "updated_at",
        )
        read_only_fields = (
            "id", "recipe", "inventory_item_name", "unit", "unit_name",
            "unit_symbol", "created_at", "updated_at",
        )

    def validate_inventory_item(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Inactive inventory items cannot be used.")
        return value


class RecipeSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id", "product", "product_name", "name", "instructions",
            "servings", "preparation_time_minutes", "cooking_time_minutes",
            "is_active", "ingredients", "created_by", "created_at", "updated_at",
        )
        read_only_fields = (
            "id", "product_name", "ingredients", "created_by",
            "created_at", "updated_at",
        )

    def validate_product(self, value):
        if not value.is_available:
            raise serializers.ValidationError("A recipe requires an available product.")
        return value
