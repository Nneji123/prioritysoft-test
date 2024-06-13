"""
signals.py file for inventory app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Supplier
from .tasks import send_new_supplier_notification


@receiver(post_save, sender=Supplier)
def supplier_notification(sender, instance, created, **kwargs):
    if created:
        send_new_supplier_notification.delay(supplier_id=instance.id)
