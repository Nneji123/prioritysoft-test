import sys
import os

import pytest

pytest_plugins = ('celery.contrib.pytest', )

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://localhost:6379',
        'result_backend': 'redis://localhost:6379'
    }


# Add the apps directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "apps"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "staticfiles"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "static"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings.development")