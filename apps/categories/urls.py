from rest_framework.routers import DefaultRouter

from apps.catalog.views import CatalogView

from .views import CategoryViewSet
from .views import CategoryListWithProductsAPIView
from django.urls import path
router = DefaultRouter()
router.register("", CategoryViewSet, basename="category")

urlpatterns = [
    path("dashboard/", CategoryListWithProductsAPIView.as_view(), name="categories-with-products"),
    
]
urlpatterns += router.urls
