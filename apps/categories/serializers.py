from rest_framework import serializers

from .models import Category
from apps.products.models import Product
from apps.products.models import Ingredient
def get_secure_image_url(request, image):
    if not image:
        return None

    url = image.url

    if request:
        url = request.build_absolute_uri(url)

    return url.replace("http://", "https://", 1)

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
    image = serializers.SerializerMethodField()
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
    def get_image(self, obj):
        request = self.context.get("request")
        return get_secure_image_url(request, obj.image)

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
        