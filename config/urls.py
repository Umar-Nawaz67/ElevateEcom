from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/services/", include("apps.services.urls")),
    path("api/v1/categories/", include("apps.categories.urls")),
    path("api/v1/packages/", include("apps.packages.urls")),
    path("api/v1/products/", include("apps.products.urls")),
    path("api/v1/catalog/", include("apps.catalog.urls")),
    path("api/v1/orders/", include("apps.orders.urls")),
]
