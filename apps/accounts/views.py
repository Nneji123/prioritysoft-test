"""
views.py file for accounts app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.models import get_token_model
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.views import PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import login as django_login
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .mixins import CustomResponseMixin
from .schema import (
    change_password_schema,
    confirm_password_reset_schema,
    login_schema,
    reset_password_schema,
)
from .serializers import (
    CustomLoginSerializer,
    CustomPasswordChangeSerializer,
    CustomPasswordResetConfirmSerializer,
    CustomPasswordResetSerializer,
)
from .throttles import PasswordChangeThrottle, PasswordResetThrottle


@login_schema
class CustomLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomLoginSerializer
    throttle_scope = "dj_rest_auth"

    user = None
    access_token = None
    token = None

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if api_settings.USE_JWT:
            if api_settings.JWT_AUTH_RETURN_EXPIRATION:
                response_serializer = api_settings.JWT_SERIALIZER_WITH_EXPIRATION
            else:
                response_serializer = api_settings.JWT_SERIALIZER
        else:
            response_serializer = api_settings.TOKEN_SERIALIZER
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data["user"]
        token_model = get_token_model()

        if api_settings.USE_JWT:
            self.access_token, self.refresh_token = jwt_encode(self.user)
        elif token_model:
            self.token = api_settings.TOKEN_CREATOR(
                token_model, self.user, self.serializer
            )

        if api_settings.SESSION_LOGIN:
            self.process_login()

    def get_response(self, response_code=status.HTTP_200_OK):
        serializer_class = self.get_response_serializer()
        if api_settings.USE_JWT:
            from rest_framework_simplejwt.settings import api_settings as jwt_settings

            access_token_expiration = (
                timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
            )
            refresh_token_expiration = (
                timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
            )
            return_expiration_times = api_settings.JWT_AUTH_RETURN_EXPIRATION
            auth_httponly = api_settings.JWT_AUTH_HTTPONLY
            data = {
                "user": self.user,
                "access_token": self.access_token,
            }
            if not auth_httponly:
                data["refresh_token"] = self.refresh_token
            if return_expiration_times:
                data["access_token_expiration"] = access_token_expiration
                data["refresh_token_expiration"] = refresh_token_expiration
            serializer = serializer_class(
                instance=data, context=self.get_serializer_context()
            )
        else:
            serializer = serializer_class(
                instance=self.token, context=self.get_serializer_context()
            )

        response_data = {
            "responseCode": status.HTTP_200_OK,
            "message": "Login Successful",
            "data": serializer.data,
        }

        return Response(response_data, status=response_code)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        return self.get_error_response(
            errors=exc.detail,
            response_code=response.status_code,
            message="Unable to log in with provided credentials.",
        )

    def get_error_response(self, errors, response_code=400, message=None):
        error_messages = []

        def extract_error_messages(errors):
            if isinstance(errors, dict):
                for error_detail in errors.values():
                    if isinstance(error_detail, list):
                        for detail in error_detail:
                            if isinstance(detail, ErrorDetail):
                                error_messages.append(detail)
                            else:
                                error_messages.append(str(detail))
                    else:
                        error_messages.append(str(error_detail))
            else:
                error_messages.append(str(errors))

        extract_error_messages(errors)

        final_message = (
            message if message else "; ".join(str(msg) for msg in error_messages)
        )

        return Response(
            {"responseCode": response_code, "message": final_message, "data": {}},
            status=response_code,
        )


@change_password_schema
class CustomPasswordChangeView(CustomResponseMixin, PasswordChangeView):
    serializer_class = CustomPasswordChangeSerializer
    throttle_classes = [PasswordChangeThrottle]

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return self.get_response(
                response.data,
                response_code=response.status_code,
                message="Password changed successfully",
            )
        except ValidationError as exc:
            # Pass a custom error message here if needed
            custom_message = self.get_custom_error_message(exc.detail)
            return self.get_error_response(
                exc.detail, response_code=exc.status_code, message=custom_message
            )
        except Exception as exc:
            response = self.handle_exception(exc)
            return response


@confirm_password_reset_schema
class CustomPasswordResetConfirmView(CustomResponseMixin, PasswordResetConfirmView):
    serializer_class = CustomPasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return self.get_response(
                response.data,
                response_code=response.status_code,
                message="Password reset confirmation successful",
            )
        except ValidationError as exc:
            custom_message = self.get_custom_error_message(exc.detail)
            return self.get_error_response(
                exc.detail, response_code=exc.status_code, message=custom_message
            )
        except Exception as exc:
            response = self.handle_exception(exc)
            return response


@reset_password_schema
class CustomPasswordResetView(CustomResponseMixin, GenericAPIView):
    throttle_classes = [PasswordResetThrottle]
    serializer_class = CustomPasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return self.get_response(
                {"detail": "Password reset e-mail has been sent."},
                response_code=status.HTTP_200_OK,
                message="Password reset email sent successfully",
            )
        except ValidationError as exc:
            custom_message = self.get_custom_error_message(exc.detail)
            return self.get_error_response(
                exc.detail, response_code=exc.status_code, message=custom_message
            )
        except Exception as exc:
            response = self.handle_exception(exc)
            return response
