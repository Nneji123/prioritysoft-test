"""
admin.py file for accounts app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_employee", "is_admin")
    search_fields = ("email", "first_name", "last_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_admin:
            return qs
        return qs.none()

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_admin


admin.site.register(CustomUser, CustomUserAdmin)
