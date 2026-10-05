from rest_framework import serializers

from .models import Category
from apps.products.models import Product
from apps.products.models import Ingredient


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
        ]

class ProductSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'duration_minutes',
            'image',
            'is_active',
            'sort_order',
            'ingredients',
        ]


class CategoryWithProductsSerializer(serializers.ModelSerializer):
    # Uses the related_name="products" from Product.category
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'image',
            'is_active',
            'sort_order',
            'products',
        ]
        