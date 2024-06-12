import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from loguru import logger
from core.logger import loguru_logging_middleware

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def get_response():
    return lambda request: HttpResponse("Response content")

@pytest.mark.django_db
def test_loguru_logging_middleware(request_factory, get_response, caplog):
    request = request_factory.get('/test-path')
    middleware = loguru_logging_middleware(get_response)
    
    with caplog.at_level('INFO', logger="my_module"):
        response = middleware(request)
    
    assert response.status_code == 200
    assert "Request: GET /test-path" in caplog.text
    assert "Response: 200 b'Response content'" in caplog.text