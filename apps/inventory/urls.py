"""
urls.py file for inventory app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r"items", ItemViewSet)
router.register(r"suppliers", SupplierViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
