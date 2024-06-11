# accounts/management/commands/create_predefined_users.py
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

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
                "email": "superuser@example.com",
                "password": "password123",
                "role": "superuser",
            },
        ]

        for user_data in predefined_users:
            email = user_data["email"]
            password = user_data["password"]
            role = user_data["role"]

            if role == "superuser":
                user = CustomUser.objects.create_superuser(
                    email=email, password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        _("Successfully created superuser: {}".format(email))
                    )
                )
            elif role == "admin":
                user = CustomUser.objects.create_admin(email=email, password=password)
                self.stdout.write(
                    self.style.SUCCESS(
                        _("Successfully created admin: {}".format(email))
                    )
                )
            elif role == "employee":
                user = CustomUser.objects.create_employee(
                    email=email, password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        _("Successfully created employee: {}".format(email))
                    )
                )
            else:
                user = CustomUser.objects.create_user(email=email, password=password)
                self.stdout.write(
                    self.style.SUCCESS(_("Successfully created user: {}".format(email)))
                )
