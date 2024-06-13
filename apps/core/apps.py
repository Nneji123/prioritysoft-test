"""
apps.py file for core app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
