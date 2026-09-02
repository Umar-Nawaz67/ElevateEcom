from django.contrib import admin
from .models import Service
from apps.packages.models import Package


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