"""
permissions.py file for inventory app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create, update, and delete suppliers.
    Employees can only view.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_admin
