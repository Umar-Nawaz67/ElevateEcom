from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.serializers import OrderSerializer
from .models import Order, User  # Import your User model


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Allow STAFF and ADMIN roles to access all orders
        if user.role in [User.Roles.STAFF, User.Roles.ADMIN]:
            return Order.objects.select_related("package", "customer")

        return Order.objects.filter(customer=user)

    def partial_update(self, request, *args, **kwargs):
        # Restrict status changes to STAFF and ADMIN
        if request.user.role not in [User.Roles.STAFF, User.Roles.ADMIN]:
            return Response({"detail": "Staff only"}, status=403)

        o = self.get_object()
        new = request.data.get("status")
        allowed = {
            "PENDING": ["ACCEPTED", "CANCELLED"],
            "ACCEPTED": ["IN_PROGRESS", "CANCELLED"],
            "IN_PROGRESS": ["COMPLETED"],
            "COMPLETED": [],
            "CANCELLED": [],
        }

        if new not in allowed.get(o.status, []):
            return Response({"detail": "Invalid status transition"}, status=400)

        o.status = new
        o.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(o).data)