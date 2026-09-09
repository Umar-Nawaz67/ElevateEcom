from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Service
from .serializers import ServiceSerializer
from .models import PromotionImage
from .serializers import PromotionImageSerializer
from .permissions import IsAdminOrStaff
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
class ServiceViewSet(viewsets.ModelViewSet):
 serializer_class=ServiceSerializer; permission_classes=[IsAuthenticated]
 def get_queryset(self): return Service.objects.all() if self.request.user.is_staff else Service.objects.filter(is_active=True)
 def get_permissions(self): return [IsAuthenticated(),IsAdminUser()] if self.action in ['create','update','partial_update','destroy'] else [IsAuthenticated()]
# Admin API: Add, Update, Delete, List all promotion images
User = get_user_model()
class PromotionViewSet(viewsets.ModelViewSet):
    serializer_class = PromotionImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        """Allow public access for read-only actions; require Admin/Staff for modifications."""
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminOrStaff()]

    def get_queryset(self):
        """Public users see active banners; Staff/Admin see all banners."""
        user = self.request.user
        if user.is_authenticated and user.role in [User.Roles.ADMIN, User.Roles.STAFF]:
            return PromotionImage.objects.all()
        return PromotionImage.objects.filter(is_active=True)