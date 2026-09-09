from django.contrib import admin
from .models import Service
from apps.packages.models import Package
from django.contrib import admin
from django.utils.html import mark_safe
from .models import PromotionImage

class PackageInline(admin.TabularInline):
    model = Package
    extra = 1

    fields = (
        "name",
        "description",
        "price",
        "duration_minutes",
        "image",
        "is_active",
    )

    show_change_link = True


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "package_count",
        "is_active",
        "sort_order",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "is_active",
        "sort_order",
    )

    ordering = (
        "sort_order",
        "name",
    )

    inlines = [
        PackageInline,
    ]

    fieldsets = (
        (
            "Service Information",
            {
                "fields": (
                    "name",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Display Settings",
            {
                "fields": (
                    "is_active",
                    "sort_order",
                )
            },
        ),
    )

    @admin.display(description="Packages")
    def package_count(self, obj):
        return obj.packages.count()





@admin.register(PromotionImage)
class PromotionImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "title",
        "is_active",
        "link_url",
        "created_at",
    )
    list_editable = ("is_active",)
    list_filter = ("is_active", "created_at")
    search_fields = ("title",)
    readonly_fields = ("image_preview_large", "created_at")

    fieldsets = (
        (None, {
            "fields": ("title", "image", "image_preview_large", "link_url", "is_active")
        }),
        ("Timestamps", {
            "fields": ("created_at",),
        }),
    )

    def image_preview(self, obj):
        """Thumbnail preview for the table list view."""
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="height: 40px; width: auto; border-radius: 4px;" />'
            )
        return "No Image"

    image_preview.short_description = "Preview"

    def image_preview_large(self, obj):
        """Larger image preview for the detail view."""
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 200px; width: auto; border-radius: 8px;" />'
            )
        return "No Image"

    image_preview_large.short_description = "Image Preview"    