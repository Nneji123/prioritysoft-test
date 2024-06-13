"""
urls.py file for accounts app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from dj_rest_auth.jwt_auth import get_refresh_view
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    CustomLoginView,
    CustomPasswordChangeView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
)

urlpatterns = [
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path(
        "auth/password/change/",
        CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "auth/password/reset/confirm/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "auth/password/reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
]

urlpatterns += [
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
]
