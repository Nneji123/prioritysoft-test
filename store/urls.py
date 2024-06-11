# store_management/urls.py
from accounts.views import UserViewSet
from django.contrib import admin
from django.urls import include, path
from inventory.views import ItemViewSet, SupplierViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"items", ItemViewSet)
router.register(r"suppliers", SupplierViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_auth.urls")),
    path("api/auth/registration/", include("rest_auth.registration.urls")),
]
