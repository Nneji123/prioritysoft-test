# accounts/management/commands/customcreatesuperuser.py

import os

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from dotenv import load_dotenv

load_dotenv()

CustomUser = get_user_model()


class Command(BaseCommand):
    help = "Create predefined users"

    def handle(self, *args, **kwargs):
        predefined_users = [
            {"email": "user@example.com", "password": "password123", "role": "user"},
            {
                "email": "employee@example.com",
                "password": "password123",
                "role": "employee",
            },
            {"email": "admin@example.com", "password": "password123", "role": "admin"},
            {
                "email": os.environ.get("SUPERUSER_EMAIL"),
                "password": os.environ.get("SUPERUSER_PASSWORD"),
                "role": "superuser",
            },
        ]

        for user_data in predefined_users:
            email = user_data["email"]
            password = user_data["password"]
            role = user_data["role"]

            if CustomUser.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"User with email {email} already exists, skipping..."
                    )
                )
                continue

            user = self.create_user_by_role(email, password, role)
            self.create_email_address(user)

    def create_user_by_role(self, email, password, role):
        if role == "superuser":
            user = CustomUser.objects.create_superuser(email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(
                    _("Successfully created superuser: {}".format(email))
                )
            )
        elif role == "admin":
            user = CustomUser.objects.create_admin(email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(_("Successfully created admin: {}".format(email)))
            )
        elif role == "employee":
            user = CustomUser.objects.create_employee(email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(_("Successfully created employee: {}".format(email)))
            )
        else:
            user = CustomUser.objects.create_user(email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(_("Successfully created user: {}".format(email)))
            )
        return user

    def create_email_address(self, user):
        email_address, email_created = EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            defaults={"primary": True, "verified": True},
        )
        if email_created:
            self.stdout.write(self.style.SUCCESS("Email address created and verified!"))
