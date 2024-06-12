# tests/conftest.py
import sys
import os

# Add the apps directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "apps"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "staticfiles"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "static"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings.development")