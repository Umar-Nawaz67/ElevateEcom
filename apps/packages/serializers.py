from rest_framework import serializers

from apps.services.models import Service
from .models import Package
class PackageSerializer(serializers.ModelSerializer):
 class Meta: model=Package; fields='__all__'
class ServiceWithPackagesSerializer(serializers.ModelSerializer):
    # Matches the related_name='packages' in Package.service
    packages = PackageSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'packages']  # Adjust fields based on your Service model