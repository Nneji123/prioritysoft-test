"""
models.py file for accounts app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager
from .utils import validate_four_digit_number


class CustomUser(AbstractUser):
    username = None

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    email = models.EmailField(unique=True)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class PasswordResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField(
        validators=[validate_four_digit_number], null=True, blank=True
    )
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
