from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role in [User.Roles.ADMIN, User.Roles.STAFF]
        )

class StaffWriteMixin:
    """Any authenticated user can read; only Django staff can create/update/delete."""

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser, IsAuthenticated

        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]
