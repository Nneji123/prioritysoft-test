"""
serializers.py file for accounts app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

import random
from datetime import timedelta

from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import CustomUser, PasswordResetCode
from .tasks import send_password_reset_email
from .utils import validate_four_digit_number


class CustomLoginSerializer(LoginSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password")

    username = None
    email = serializers.EmailField(required=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserAuthMessageSerializer(serializers.Serializer):
    responseCode = serializers.CharField()
    message = serializers.CharField()
    data = serializers.JSONField()


class UserAuthErrorSerializer(serializers.Serializer):
    responseCode = serializers.CharField()
    message = serializers.CharField()
    data = serializers.JSONField()


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    """
    Custom password change serializer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(
        validators=[validate_four_digit_number], required=True
    )
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        new_password1 = attrs.get("new_password1")
        new_password2 = attrs.get("new_password2")

        # Check if the passwords match
        if new_password1 != new_password2:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )

        # Check if the email exists
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                _("The provided email address does not belong to any account.")
            )

        # Validate the OTP
        try:
            reset_code = PasswordResetCode.objects.get(user=user, code=code)
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError(_("Invalid code."))

        if reset_code.is_expired():
            raise serializers.ValidationError(_("The code has expired."))

        # Set the user on the serializer
        attrs["user"] = user
        attrs["reset_code"] = reset_code  # Store reset code for deletion later
        return attrs

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password1"]
        user.set_password(new_password)
        user.save()

        self.delete_reset_code()

        return user

    def delete_reset_code(self):
        reset_code = self.validated_data["reset_code"]
        reset_code.delete()


class CustomPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    reset_form = None

    @property
    def password_reset_form_class(self):
        if "allauth" in settings.INSTALLED_APPS:
            from allauth.account.forms import (
                ResetPasswordForm as AllAuthPasswordResetForm,
            )

            return AllAuthPasswordResetForm
        else:
            from django.contrib.auth.forms import PasswordResetForm

            return PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        # Check if the user exists
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "The provided email address does not belong to any account."
            )

        return value

    def save(self):
        email = self.validated_data["email"]
        user = CustomUser.objects.get(email=email)
        # Generate 4-digit Code for Password Reset
        code = random.randint(1000, 9999)
        PasswordResetCode.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=5),
        )
        send_password_reset_email.delay(email, code)

        return email
