from django.db import models

from apps.categories.models import Category
from apps.packages.models import Package


class Ingredient(models.Model):
    """Reusable master list of ingredients (shared by many products)."""

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

from django.db import models


class Product(models.Model):
    """A product that belongs to a category and can be ordered by a customer."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(default=60)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through="ProductIngredient",
        related_name="products",
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class ProductIngredient(models.Model):
    """Product <-> Ingredient link with quantity and 'removable by customer' flag."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, related_name="product_links"
    )
    quantity = models.CharField(
        max_length=50, blank=True, help_text='Free text, e.g. "200 g" or "2 slices"'
    )
    is_optional = models.BooleanField(
        default=False, help_text="Customer may remove this ingredient when ordering"
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "ingredient"], name="unique_ingredient_per_product"
            )
        ]

    def __str__(self):
        return f"{self.product.name}: {self.ingredient.name}"
