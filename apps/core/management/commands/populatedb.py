"""
populatedb.py file for commands app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.apps import apps
from django.core.management.base import BaseCommand
from django_seed import Seed


class Command(BaseCommand):
    help = "Populates the database with fake data for models in the inventory app"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            help="Number of records to create for each model",
            default=10,
        )

    def handle(self, *args, **options):
        number = options["number"]
        seeder = Seed.seeder()
        inventory_app_models = apps.get_app_config("inventory").get_models()

        for model in inventory_app_models:
            self.stdout.write(f"Creating {number} fake records for {model.__name__}...")
            seeder.add_entity(model, number)

        inserted_pks = seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated the database with {sum(len(ids) for ids in inserted_pks.values())} records from the inventory app"
            )
        )
