"""
apps.py file for accounts app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
