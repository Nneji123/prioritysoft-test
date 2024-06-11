# inventory/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet, Suppli

router = DefaultRouter()
router.register(r"items", ItemViewSet)
ro

urlpatterns = [
    path("", include(router.urls)),
]
