from django.contrib import admin

from apps.products.models import Product

from .models import Package


# class ProductInline(admin.TabularInline):
#     model = Product
#     extra = 1
#     fields = ("name", "price", "duration_minutes", "image", "sort_order", "is_active")
#     show_change_link = True


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "category", "product_count", "is_active", "sort_order", "created_at")
    list_filter = ("service", "category", "is_active")
    search_fields = ("name", "description", "service__name", "category__name")
    list_editable = ("is_active", "sort_order")
    ordering = ("service", "sort_order", "name")
    autocomplete_fields = ("service", "category")
    # inlines = [ProductInline]

    fieldsets = (
        ("Package Information", {"fields": ("service", "category", "name", "description", "image")}),
        ("Display Settings", {"fields": ("is_active", "sort_order")}),
    )

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()
