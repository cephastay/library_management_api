from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    """
    Custom admin class for managing the CustomUser model in the Django admin interface.
    Customizes the default UserAdmin to include email as the primary identifier and adds additional fields like 'bio'.
    """

    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None

    # Define the fields and groups displayed on the user detail page.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "bio")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Define the fields displayed on the 'Add User' page.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


    list_display = ("email", "first_name", "last_name", "bio", "is_staff")

    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    search_fields = ("first_name", "last_name", "email")

    ordering = ("email",)

    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    # Specify forms used for user creation and modification.
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

from accounts.models import LibraryProfile
@admin.register(LibraryProfile)
class LibraryProfileAdmin(admin.ModelAdmin):
    pass