from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "product_name", "unit_price", "quantity", "line_total", "removed_ingredients", "notes")
    readonly_fields = ("line_total",)
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number", "customer", "items_summary", "total_amount",
        "booking_date", "booking_time", "status", "created_at",
    )
    list_filter = ("status", "booking_date")
    search_fields = (
        "order_number", "customer__username", "customer__email",
        "customer_name", "phone", "address", "items__product_name",
    )
    readonly_fields = ("order_number", "total_amount", "created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 25
    inlines = [OrderItemInline]

    fieldsets = (
        ("Order Information", {"fields": ("order_number", "customer", "total_amount", "status")}),
        ("Customer Information", {"fields": ("customer_name", "phone", "address")}),
        ("Booking", {"fields": ("booking_date", "booking_time", "notes")}),
        ("System", {"fields": ("created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items")

    @admin.display(description="Items")
    def items_summary(self, obj):
        return ", ".join(f"{i.quantity}x {i.product_name}" for i in obj.items.all()) or "-"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.recalculate_total()
