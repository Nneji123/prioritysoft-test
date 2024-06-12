import pytest
from django.core.exceptions import ValidationError
from accounts.utils import validate_four_digit_number

@pytest.mark.parametrize("value", [1000, 1234, 9999])
def test_valid_four_digit_numbers(value):
    # This should not raise any exception
    validate_four_digit_number(value)

@pytest.mark.parametrize("value", [999, 10000, -1234, None])
def test_invalid_four_digit_numbers(value):
    with pytest.raises(ValidationError) as exc_info:
        validate_four_digit_number(value)
    assert exc_info.value == [f"{value} is not a 4-digit number"]