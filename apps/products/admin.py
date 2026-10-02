from django.contrib import admin

from .models import Ingredient, Product, ProductIngredient


class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient
    extra = 1
    fields = ("ingredient", "quantity", "is_optional", "sort_order")
    autocomplete_fields = ("ingredient",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "duration_minutes",
        "is_active",
        "sort_order",
    )

    list_editable = (
        "price",
        "is_active",
        "sort_order",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
        "category__name",
    )

    ordering = (
        "category",
        "sort_order",
        "name",
    )

    autocomplete_fields = ("category",)

    inlines = [ProductIngredientInline]

    fieldsets = (
        (
            "Product Information",
            {
                "fields": (
                    "category",
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
            "Display Settings",
            {
                "fields": (
                    "is_active",
                    "sort_order",
                )
            },
        ),
    )