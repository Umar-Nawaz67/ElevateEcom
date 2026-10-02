from rest_framework import serializers

from .models import Category
from apps.products.models import Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"




class ProductSerializer(serializers.ModelSerializer):
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