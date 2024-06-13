"""
admin.py file for inventory app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Item, Supplier

CustomUser = get_user_model()


class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "email_address", "phone_number", "date_added")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_admin:
            return qs
        if request.user.is_employee:
            return qs.none()
        return qs.none()

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_admin


class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "date_added")
    filter_horizontal = ("suppliers",)


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Item, ItemAdmin)
