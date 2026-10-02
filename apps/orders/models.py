from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string

from apps.products.models import Product


class Order(models.Model):
    """Order header. What was bought lives in OrderItem rows."""

    class Status(models.TextChoices):
        PENDING = "PENDING"
        ACCEPTED = "ACCEPTED"
        IN_PROGRESS = "IN_PROGRESS"
        COMPLETED = "COMPLETED"
        CANCELLED = "CANCELLED"

    order_number = models.CharField(max_length=30, unique=True, editable=False)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders"
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    customer_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            while True:
                number = "ELV-" + get_random_string(8, "0123456789")
                if not Order.objects.filter(order_number=number).exists():
                    self.order_number = number
                    break
        super().save(*args, **kwargs)

    def recalculate_total(self):
        total = sum((i.line_total for i in self.items.all()), Decimal("0"))
        self.total_amount = total
        self.save(update_fields=["total_amount", "updated_at"])
        return total


class OrderItem(models.Model):
    """One product line of an order. Name/price are snapshotted at order time."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items"
    )
    product_name = models.CharField(max_length=160, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    line_total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, editable=False
    )
    removed_ingredients = models.JSONField(
        default=list,
        blank=True,
        help_text="Names of optional ingredients the customer asked to leave out",
    )
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.quantity} x {self.product_name or self.product_id}"

    def save(self, *args, **kwargs):
        if not self.product_name:
            self.product_name = self.product.name
        if self.unit_price is None:
            self.unit_price = self.product.price
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)
