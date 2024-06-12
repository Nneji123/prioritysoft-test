# accounts/utils.py

from django.core.exceptions import ValidationError


def validate_four_digit_number(value):
    if value is not None and (value < 1000 or value > 9999):
        raise ValidationError(f"{value} is not a 4-digit number")
