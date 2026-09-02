from django.contrib import admin
from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "service",
        "price",
        "duration_minutes",
        "is_active",
        "created_at",
    )

    list_filter = (
        "service",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
        "service__name",
    )

    list_editable = (
        "price",
        "is_active",
    )

    ordering = (
        "service",
        "name",
    )

    autocomplete_fields = (
        "service",
    )

    fieldsets = (
        (
            "Package Information",
            {
                "fields": (
                    "service",
                    "name",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Pricing & Duration",
            {
                "fields": (
                    "price",
                    "duration_minutes",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                )
            },
        ),
    )