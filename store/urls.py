# store_management/urls.py
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path(f"{settings.ADMIN_URL_PATH}/", admin.site.urls),
    path("api/v1/", include("inventory.urls")),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "api/v1/docs/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="docs",
    ),
]
