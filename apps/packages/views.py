from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Package
from .serializers import PackageSerializer
class PackageViewSet(viewsets.ModelViewSet):
 serializer_class=PackageSerializer; permission_classes=[IsAuthenticated]
 def get_queryset(self): return Package.objects.select_related('service').filter(is_active=True) if not self.request.user.is_staff else Package.objects.select_related('service').all()
 def get_permissions(self): return [IsAuthenticated(),IsAdminUser()] if self.action in ['create','update','partial_update','destroy'] else [IsAuthenticated()]
