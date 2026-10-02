from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.services.permissions import StaffWriteMixin

from .models import Ingredient, Product, ProductIngredient
from .serializers import (
    IngredientSerializer,
    ProductIngredientSerializer,
    ProductSerializer,
)

class ProductViewSet(viewsets.ModelViewSet):
    """Filters: ?category=<id>"""

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Product.objects.select_related(
            "category",
        ).prefetch_related(
            "product_ingredients__ingredient"
        )

        if not self.request.user.is_staff:
            qs = qs.filter(
                is_active=True,
                category__is_active=True,
            )

        p = self.request.query_params

        if p.get("category"):
            qs = qs.filter(category_id=p["category"])

        return qs

class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        qs = Ingredient.objects.all()
        return qs if self.request.user.is_staff else qs.filter(is_active=True)


class ProductIngredientViewSet( viewsets.ModelViewSet):
    """Attach / detach / edit ingredients on a product. Filter: ?product=<id>"""

    serializer_class = ProductIngredientSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        qs = ProductIngredient.objects.select_related("ingredient", "product")
        product = self.request.query_params.get("product")
        return qs.filter(product_id=product) if product else qs
