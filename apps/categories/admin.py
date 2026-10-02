from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "package_count", "is_active", "sort_order", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    list_editable = ("is_active", "sort_order")
    ordering = ("sort_order", "name")

    @admin.display(description="Packages")
    def package_count(self, obj):
        return obj.packages.count()
