from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Service
from .serializers import ServiceSerializer
class ServiceViewSet(viewsets.ModelViewSet):
 serializer_class=ServiceSerializer; permission_classes=[IsAuthenticated]
 def get_queryset(self): return Service.objects.all() if self.request.user.is_staff else Service.objects.filter(is_active=True)
 def get_permissions(self): return [IsAuthenticated(),IsAdminUser()] if self.action in ['create','update','partial_update','destroy'] else [IsAuthenticated()]
