from django.db.models import Prefetch
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from apps.products.models import Product
from apps.services.permissions import StaffWriteMixin

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Customers see active categories; staff see all."""
    
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        qs = Category.objects.all()
        return qs if self.request.user.is_staff else qs.filter(is_active=True)

from .serializers import CategoryWithProductsSerializer


class CategoryListWithProductsAPIView(generics.ListAPIView):
    serializer_class = CategoryWithProductsSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        # Fetch active categories and prefetch active products to optimize DB queries
        active_products = Product.objects.filter(is_active=True)

        return Category.objects.filter(is_active=True).prefetch_related(
            Prefetch('products', queryset=active_products)
        )