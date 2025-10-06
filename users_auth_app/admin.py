from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["id","email", "fullname", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("fullname",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "fullname", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email", "fullname")
    filter_horizontal = ("groups", "user_permissions")

admin.site.register(User, UserAdmin)