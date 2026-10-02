from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.packages.models import Package
from apps.products.models import Product, ProductIngredient
from apps.services.models import Service

from .serializers import CatalogServiceSerializer


class CatalogView(ListAPIView):
    """Public home/dashboard payload with only active records at every level.
    Optional filter: ?category=<id> limits packages to that category."""

    serializer_class = CatalogServiceSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        products = Product.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "product_ingredients",
                queryset=ProductIngredient.objects.filter(
                    ingredient__is_active=True
                ).select_related("ingredient"),
            )
        )
        packages = Package.objects.filter(
            is_active=True, category__is_active=True
        ).select_related("category")
        category = self.request.query_params.get("category")
        if category:
            packages = packages.filter(category_id=category)
        packages = packages.prefetch_related(Prefetch("products", queryset=products))
        return Service.objects.filter(is_active=True).prefetch_related(
            Prefetch("packages", queryset=packages)
        )
