from rest_framework import serializers
from .models import Service
class ServiceSerializer(serializers.ModelSerializer):
 class Meta: model=Service; fields='__all__'
from rest_framework import serializers
from .models import PromotionImage

class PromotionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionImage
        fields = ["id", "title", "image", "link_url", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]