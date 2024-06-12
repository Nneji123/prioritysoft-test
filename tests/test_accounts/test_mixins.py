import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest.mock import Mock, patch

from accounts.mixins import CustomResponseMixin

class TestCustomResponseMixin(CustomResponseMixin):
    pass

@pytest.fixture
def mixin():
    return TestCustomResponseMixin()

def test_get_response(mixin):
    data = {"key": "value"}
    response = mixin.get_response(data, response_code=status.HTTP_201_CREATED, message="Created")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        "responseCode": status.HTTP_201_CREATED,
        "message": "Created",
        "data": data,
    }

def test_handle_exception(mixin):
    exc = ValidationError({"field": ["This field is required."]})
    mock_super = Mock()
    mock_super.handle_exception.return_value = Response(
        {"field": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST
    )
    with patch.object(TestCustomResponseMixin, 'handle_exception', mock_super.handle_exception):
        response = mixin.handle_exception(exc)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "responseCode": status.HTTP_400_BAD_REQUEST,
            "message": str(exc),
            "data": {"field": ["This field is required."]},
        }

@pytest.mark.parametrize("errors, expected_message", [
    ({"field1": ["error1"]}, "error1"),
    ({"field1": ["error1", "error2"]}, "error1; error2"),
    ({"field1": {"nested_field": ["nested_error"]}}, "nested_error"),
    (["list_error1", "list_error2"], "list_error1; list_error2"),
    (ValidationError({"field1": [ErrorDetail("error1", code="invalid")]}), "error1")
])
def test_get_custom_error_message(mixin, errors, expected_message):
    assert mixin.get_custom_error_message(errors) == expected_message