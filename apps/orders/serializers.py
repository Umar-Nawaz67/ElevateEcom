from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from apps.products.models import Product, ProductIngredient

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1, default=1)
    # write: ids of ProductIngredient rows (the `id` in product.ingredients) to leave out
    removed_ingredient_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False, default=list
    )

    class Meta:
        model = OrderItem
        fields = [
            "id", "product", "product_name", "unit_price", "quantity", "line_total",
            "removed_ingredients", "removed_ingredient_ids", "notes",
        ]
        read_only_fields = ["id", "product_name", "unit_price", "line_total", "removed_ingredients"]

    def validate_product(self, product):
        if not (product.is_active and product.category.is_active):
            raise serializers.ValidationError(f'"{product.name}" is not available.')
        return product

    def validate(self, attrs):
        ids = set(attrs.get("removed_ingredient_ids", []))
        if ids:
            optional = set(
                ProductIngredient.objects.filter(
                    product=attrs["product"], id__in=ids, is_optional=True
                ).values_list("id", flat=True)
            )
            bad = ids - optional
            if bad:
                raise serializers.ValidationError(
                    {"removed_ingredient_ids": f"Not removable for this product: {sorted(bad)}"}
                )
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "customer", "customer_name", "phone", "address",
            "booking_date", "booking_time", "notes", "status", "total_amount",
            "items", "created_at", "updated_at",
        ]
        read_only_fields = ["customer", "order_number", "total_amount", "status", "created_at", "updated_at"]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("An order needs at least one item.")
        return items

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")
        order = Order.objects.create(
            customer=self.context["request"].user, **validated_data
        )
        total = Decimal("0")
        for item in items:
            product = item["product"]
            removed_ids = item.get("removed_ingredient_ids", [])
            removed_names = list(
                ProductIngredient.objects.filter(id__in=removed_ids)
                .select_related("ingredient")
                .values_list("ingredient__name", flat=True)
            )
            line = OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                unit_price=product.price,  # price is always taken from the server
                quantity=item["quantity"],
                removed_ingredients=removed_names,
                notes=item.get("notes", ""),
            )
            total += line.line_total
        order.total_amount = total
        order.save(update_fields=["total_amount", "updated_at"])
        return order

    def update(self, instance, validated_data):
        raise serializers.ValidationError("Orders cannot be edited; only status changes are allowed.")
