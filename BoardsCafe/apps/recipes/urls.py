from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeIngredientDetailView,
    RecipeIngredientListCreateView,
    RecipeViewSet,
)

app_name = "recipes"

router = DefaultRouter()
router.register("", RecipeViewSet, basename="recipe")

urlpatterns = [
    path("<int:recipe_pk>/ingredients/", RecipeIngredientListCreateView.as_view(), name="ingredient-list-create"),
    path("<int:recipe_pk>/ingredients/<int:pk>/", RecipeIngredientDetailView.as_view(), name="ingredient-detail"),
]
urlpatterns += router.urls
