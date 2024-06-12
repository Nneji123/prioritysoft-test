import pytest
from django.test import RequestFactory
from core.middlewares import DisableCSRFMiddleware

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.mark.django_db
def test_disable_csrf_middleware(request_factory):
    middleware = DisableCSRFMiddleware()
    request = request_factory.get('/test-path')
    middleware.process_request(request)
    
    assert hasattr(request, "_dont_enforce_csrf_checks")
    assert request._dont_enforce_csrf_checks is True