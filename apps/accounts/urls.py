# accounts/urls.py

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
    path("auth/login/", CustomLoginView.as_view(), name="user_login"),
    path(
        "auth/password/change/",
        CustomPasswordChangeView.as_view(),
        name="custom_password_change",
    ),
    path(
        "auth/password/reset/confirm/",
        CustomPasswordResetConfirmView.as_view(),
        name="custom_password_reset_confirm",
    ),
    path(
        "auth/password/reset/",
        CustomPasswordResetView.as_view(),
        name="custom_password_reset",
    ),
]

urlpatterns += [
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
]