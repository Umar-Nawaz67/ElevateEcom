from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.catalog.views import CatalogView

from .views import PackageViewSet

router = DefaultRouter()
router.register("", PackageViewSet, basename="package")

urlpatterns = [
    # Kept for backwards compatibility: now returns the full
    # service -> category -> package -> product -> ingredient tree.
    path("dashboard/", CatalogView.as_view(), name="service-packages"),
]
urlpatterns += router.urls
