from django.db import models

from apps.categories.models import Category
from apps.services.models import Service


class Package(models.Model):
    """Service -> Package -> Product. A package is also tagged with a (standalone) Category."""

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="packages"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="packages"
    )
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="packages/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.service.name} - {self.name}"
