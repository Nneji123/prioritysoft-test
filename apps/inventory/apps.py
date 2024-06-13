"""
apps.py file for inventory app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"

    def ready(self):
        import inventory.signals
