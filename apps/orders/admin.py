from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer",
        "package",
        "price",
        "booking_date",
        "booking_time",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "booking_date",
    )

    search_fields = (
        "order_number",
        "customer__username",
        "customer__email",
        "customer_name",
        "phone",
        "address",
    )

    readonly_fields = (
        "order_number",
        "price",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "order_number",
                    "customer",
                    "package",
                    "price",
                    "status",
                )
            },
        ),
        (
            "Customer Information",
            {
                "fields": (
                    "customer_name",
                    "phone",
                    "address",
                )
            },
        ),
        (
            "Booking",
            {
                "fields": (
                    "booking_date",
                    "booking_time",
                    "notes",
                )
            },
        ),
        (
            "System",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )