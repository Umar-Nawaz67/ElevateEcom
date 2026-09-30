from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Package
from .serializers import PackageSerializer
from apps.services.models import Service
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .serializers import ServiceWithPackagesSerializer
class PackageViewSet(viewsets.ModelViewSet):
 serializer_class=PackageSerializer; permission_classes=[IsAuthenticated]
 def get_queryset(self): return Package.objects.select_related('service').filter(is_active=True) if not self.request.user.is_staff else Package.objects.select_related('service').all()
 def get_permissions(self): return [IsAuthenticated(),IsAdminUser()] if self.action in ['create','update','partial_update','destroy'] else [IsAuthenticated()]
class ServicePackageListView(ListAPIView):
    serializer_class = ServiceWithPackagesSerializer
    permission_classes = [AllowAny]  # No authorization required

    def get_queryset(self):
        # Fetch services along with only active packages (optional filter)
        return Service.objects.prefetch_related(
            Prefetch('packages', queryset=Package.objects.filter(is_active=True))
        )