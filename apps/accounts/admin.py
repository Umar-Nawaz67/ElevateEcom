from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import SocialAccount, User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Columns displayed in the user table view
    list_display = (
        "username",
        "email",
        "role",
        "phone",
        "is_staff",
        "registration_completed",
    )

    # Sidebar filter options
    list_filter = ("role", "is_staff", "is_superuser", "registration_completed")

    # Search bar capability
    search_fields = ("username", "email", "phone", "firebase_uid")

    # Fields displayed on the EDIT user page
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Firebase & Custom Profile",
            {
                "fields": (
                    "role",
                    "phone",
                    "firebase_uid",
                    "firebase_provider",
                    "registration_completed",
                ),
            },
        ),
    )

    # Fields displayed on the CREATE user page
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Firebase & Custom Profile",
            {
                "fields": (
                    "role",
                    "phone",
                    "firebase_uid",
                    "firebase_provider",
                    "registration_completed",
                ),
            },
        ),
    )


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "provider", "provider_user_id", "email")
    search_fields = ("email", "provider_user_id", "user__username")