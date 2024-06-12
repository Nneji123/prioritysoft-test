# inventory/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Supplier
from .tasks import send_new_supplier_notification


@receiver(post_save, sender=Supplier)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        send_new_supplier_notification.delay(supplier_id=instance.id)
