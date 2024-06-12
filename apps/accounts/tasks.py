# accounts/tasks.py

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from loguru import logger


@shared_task
def send_password_reset_email(to_email, code):
    subject = "Password Reset Requested"
    html_message = render_to_string("accounts/password_reset.html", {"code": code})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    logger.info(f"Authorized Password reset for {to_email}")
