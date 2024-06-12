# tests/conftest.py
import sys
import os

from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from ..store.celery import app as celery_app

__all__ = ("celery_app",)

# Add the apps directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "apps"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "staticfiles"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "static"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings.development")