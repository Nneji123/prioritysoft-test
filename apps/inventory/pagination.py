"""
pagination.py file for inventory app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
