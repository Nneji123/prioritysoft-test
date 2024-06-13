"""
utils.py file for accounts app.

Author(s): Ifeanyi Nneji
Date: 06/13/2024
"""

from django.core.exceptions import ValidationError


def validate_four_digit_number(value):
    if value is not None and (value < 1000 or value > 9999):
        raise ValidationError(f"{value} is not a 4-digit number")
