from rest_framework import serializers
from .models import Service
class ServiceSerializer(serializers.ModelSerializer):
 class Meta: model=Service; fields='__all__'
from rest_framework import serializers
from .models import PromotionImage

def get_secure_image_url(request, image):
    if not image:
        return None

    url = image.url

    if request:
        url = request.build_absolute_uri(url)

    return url.replace("http://", "https://", 1)

class PromotionImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PromotionImage
        fields = ["id", "title", "image", "link_url", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_image(self, obj):
        request = self.context.get("request")
        return get_secure_image_url(request, obj.image)