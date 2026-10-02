"""Read-only nested tree: Service -> Package -> Product -> Ingredient (package carries its category)."""
from rest_framework import serializers

from apps.packages.models import Package
from apps.products.models import Product, ProductIngredient
from apps.services.models import Service


class CatalogIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="ingredient.name")
    ingredient_id = serializers.IntegerField(source="ingredient.id")

    class Meta:
        model = ProductIngredient
        fields = ["id", "ingredient_id", "name", "quantity", "is_optional"]


class CatalogProductSerializer(serializers.ModelSerializer):
    ingredients = CatalogIngredientSerializer(source="product_ingredients", many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "duration_minutes", "image", "ingredients"]


class CatalogPackageSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    products = CatalogProductSerializer(many=True)

    class Meta:
        model = Package
        fields = ["id", "name", "description", "image", "category", "category_name", "products"]


class CatalogServiceSerializer(serializers.ModelSerializer):
    packages = CatalogPackageSerializer(many=True)

    class Meta:
        model = Service
        fields = ["id", "name", "description", "image", "packages"]
