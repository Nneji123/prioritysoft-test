# inventory/tasks.py

from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_new_supplier_notification(supplier_id):
    from .models import Supplier

    try:
        supplier = Supplier.objects.get(id=supplier_id)
        user_model = get_user_model()
        recipients = user_model.objects.filter(is_active=True).values_list(
            "email", flat=True
        )

        subject = "New Supplier Created"
        message = render_to_string(
            "inventory/supplier_notification.html",
            {
                "supplier": supplier,
                "year": datetime.now().year,
            },
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=message,
        )
    except Supplier.DoesNotExist:
        pass
