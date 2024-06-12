import pytest
from rest_framework.response import Response
from inventory.utils import format_response

def test_format_response_with_data():
    response = format_response(200, "Success", {"key": "value"})
    assert isinstance(response, Response)
    assert response.data == {"responseCode": 200, "message": "Success", "data": {"key": "value"}}

def test_format_response_without_data():
    response = format_response(200, "Success")
    assert isinstance(response, Response)
    assert response.data == {"responseCode": 200, "message": "Success", "data": {}}
  
