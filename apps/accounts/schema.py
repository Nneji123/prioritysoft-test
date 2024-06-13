# accounts/schema.py

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status

from apps.core.utils import get_code_samples

from .serializers import (
    CustomPasswordResetConfirmSerializer,
    CustomPasswordResetSerializer,
    UserAuthErrorSerializer,
    UserAuthMessageSerializer,
)

login_schema = extend_schema_view(
    post=extend_schema(
        summary="Login",
        description="Log in an existing user.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserAuthMessageSerializer,
                description="Login Successful",
                examples=[
                    OpenApiExample(
                        name="LoginSuccessfulExample",
                        value={
                            "responseCode": 200,
                            "message": "Login Successful",
                            "data": {
                                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                "user": {
                                    "pk": "1",
                                    "email": "ifeanyinneji777@gmail.com",
                                    "first_name": "",
                                    "last_name": "",
                                },
                            },
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="accountsError400Example",
                        value={
                            "responseCode": 400,
                            "message": "Unable to log in with provided credentials.",
                            "data": {},
                        },
                    )
                ],
            ),
        },
        extensions={
            "x-code-samples": get_code_samples(
                app_name="accounts", view_name="login_view"
            ),
        },
    ),
)

change_password_schema = extend_schema_view(
    post=extend_schema(
        summary="Change Password",
        description="Change the password of the authenticated user.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserAuthMessageSerializer,
                description="Password changed successfully",
                examples=[
                    OpenApiExample(
                        name="PasswordChangeSuccessfulExample",
                        value={
                            "responseCode": 200,
                            "message": "Password changed successfully.",
                            "data": {},
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="PasswordChangeError400Example",
                        value={
                            "responseCode": 400,
                            "message": "Invalid password. Please try again.",
                            "data": {},
                        },
                    )
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Unauthorized",
                examples=[
                    OpenApiExample(
                        name="PasswordChangeError401Example",
                        value={
                            "responseCode": 401,
                            "message": "Authentication credentials were not provided.",
                            "data": {},
                        },
                    )
                ],
            ),
        },
        extensions={
            "x-code-samples": get_code_samples(
                app_name="accounts", view_name="change_password_view"
            ),
        },
    ),
)

reset_password_schema = extend_schema_view(
    post=extend_schema(
        summary="Reset Password",
        description="Request a password reset email.",
        request=CustomPasswordResetSerializer,
        examples=[
            OpenApiExample(
                name="PasswordResetRequestExample",
                value={"email": "user@example.com"},
                request_only=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserAuthMessageSerializer,
                description="Password reset email sent successfully.",
                examples=[
                    OpenApiExample(
                        name="PasswordResetSuccessExample",
                        value={
                            "responseCode": 200,
                            "message": "Password reset email sent successfully.",
                            "data": {},
                        },
                    ),
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="PasswordResetError400Example",
                        value={
                            "responseCode": 400,
                            "message": "Email address not found.",
                            "data": {},
                        },
                    ),
                ],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="ServerErrorExample",
                        value={
                            "responseCode": 500,
                            "message": "Internal server error.",
                            "data": {},
                        },
                    ),
                ],
            ),
        },
        extensions={
            "x-code-samples": get_code_samples(
                app_name="accounts", view_name="reset_password_view"
            ),
        },
    ),
)

confirm_password_reset_schema = extend_schema_view(
    post=extend_schema(
        summary="Confirm Password Reset",
        description="Confirm the password reset with a new password.",
        request=CustomPasswordResetConfirmSerializer,  # Specify the request serializer
        examples=[
            OpenApiExample(
                name="ConfirmPasswordResetExample",
                value={
                    "email": "user@example.com",
                    "code": 1234,
                    "new_password1": "newpassword",
                    "new_password2": "newpassword",
                },
                request_only=True,  # Indicate that this example is for the request payload
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserAuthMessageSerializer,
                description="Password reset confirmed.",
                examples=[
                    OpenApiExample(
                        name="ConfirmPasswordResetSuccessExample",
                        value={
                            "responseCode": 200,
                            "message": "Password reset confirmed.",
                            "data": {},
                        },
                    ),
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="ConfirmPasswordResetError400Example",
                        value={
                            "responseCode": 400,
                            "message": "Invalid code or email address.",
                            "data": {},
                        },
                    ),
                ],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="ServerErrorExample",
                        value={
                            "responseCode": 500,
                            "message": "Internal server error.",
                            "data": {},
                        },
                    ),
                ],
            ),
        },
        extensions={
            "x-code-samples": get_code_samples(
                app_name="accounts", view_name="reset_password_confirm_view"
            ),
        },
    ),
)

confirm_password_reset_schema = extend_schema_view(
    post=extend_schema(
        summary="Confirm Password Reset",
        description="Confirm the password reset with a new password.",
        request=CustomPasswordResetConfirmSerializer,  # Specify the request serializer
        examples=[
            OpenApiExample(
                name="ConfirmPasswordResetExample",
                value={
                    "email": "user@example.com",
                    "code": 1234,
                    "new_password1": "newpassword",
                    "new_password2": "newpassword",
                },
                request_only=True,  # Indicate that this example is for the request payload
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserAuthMessageSerializer,
                description="Password reset confirmed.",
                examples=[
                    OpenApiExample(
                        name="ConfirmPasswordResetSuccessExample",
                        value={
                            "responseCode": 200,
                            "message": "Password reset confirmed.",
                            "data": {},
                        },
                    ),
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="ConfirmPasswordResetError400Example",
                        value={
                            "responseCode": 400,
                            "message": "Invalid code or email address.",
                            "data": {},
                        },
                    ),
                ],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=UserAuthErrorSerializer,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="ServerErrorExample",
                        value={
                            "responseCode": 500,
                            "message": "Internal server error.",
                            "data": {},
                        },
                    ),
                ],
            ),
        },
        extensions={
            "x-code-samples": get_code_samples(
                app_name="accounts", view_name="reset_password_confirm_view"
            ),
        },
    ),
)
