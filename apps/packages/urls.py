from rest_framework.routers import DefaultRouter, path
from .views import PackageViewSet, ServicePackageListView

router = DefaultRouter()
router.register("", PackageViewSet, basename="package")
urlpatterns = [
    path(
        "dashboard/",
        ServicePackageListView.as_view(),
        name="service-packages",
    ),
]

urlpatterns += router.urls