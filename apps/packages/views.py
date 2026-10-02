from rest_framework import viewsets

from apps.services.permissions import StaffWriteMixin

from .models import Package
from .serializers import PackageSerializer


class PackageViewSet(StaffWriteMixin, viewsets.ModelViewSet):
    """Customers see active packages; staff see all. Filters: ?service=<id>&category=<id>"""

    serializer_class = PackageSerializer

    def get_queryset(self):
        qs = Package.objects.select_related("service", "category")
        if not self.request.user.is_staff:
            qs = qs.filter(
                is_active=True,
                service__is_active=True,
                category__is_active=True,
            )
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category_id=category)
        service = self.request.query_params.get("service")
        if service:
            qs = qs.filter(service_id=service)
        return qs
