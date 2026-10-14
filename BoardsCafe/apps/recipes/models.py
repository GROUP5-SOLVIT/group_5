from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Recipe(models.Model):
    product = models.OneToOneField(
        "menu.Product",
        on_delete=models.PROTECT,
        related_name="recipe",
    )
    name = models.CharField(max_length=150)
    instructions = models.TextField(blank=True)
    servings = models.PositiveIntegerField(default=1)
    preparation_time_minutes = models.PositiveIntegerField(default=0)
    cooking_time_minutes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_cafe_recipes",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product__name"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    inventory_item = models.ForeignKey(
        "inventory.InventoryItem",
        on_delete=models.PROTECT,
        related_name="recipe_ingredients",
    )
    quantity_required = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["inventory_item__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "inventory_item"],
                name="recipe_unique_inventory_ingredient",
            ),
            models.CheckConstraint(
                condition=Q(quantity_required__gt=0),
                name="recipe_ingredient_quantity_positive",
            ),
        ]

    def __str__(self):
        return f"{self.recipe.name}: {self.inventory_item.name}"
