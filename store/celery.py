import os
import sys

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "staticfiles"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "static"))

environment = os.environ.get("ENVIRONMENT")
if environment == "Prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings.development")

app = Celery("store")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
