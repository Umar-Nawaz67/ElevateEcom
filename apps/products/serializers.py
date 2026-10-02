from rest_framework import serializers

from .models import Ingredient, Product, ProductIngredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class ProductIngredientSerializer(serializers.ModelSerializer):
    """Read/write link. `id` is what the order API expects in `removed_ingredients`."""

    ingredient_name = serializers.CharField(source="ingredient.name", read_only=True)

    class Meta:
        model = ProductIngredient
        fields = ["id", "product", "ingredient", "ingredient_name", "quantity", "is_optional", "sort_order"]


class ProductSerializer(serializers.ModelSerializer):
    ingredients = ProductIngredientSerializer(
        source="product_ingredients",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "duration_minutes",
            "image",
            "is_active",
            "sort_order",
            "ingredients",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
