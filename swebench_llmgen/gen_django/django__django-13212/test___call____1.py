import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def test_regex_validator_call_valid_input():
    validator = RegexValidator(regex=r'^\d+$', message='Invalid input', code='invalid')
    value = '123456'
    try:
        validator(value)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly")

def test_regex_validator_call_invalid_input():
    validator = RegexValidator(regex=r'^\d+$', message='Invalid input', code='invalid')
    value = 'abc123'
    with pytest.raises(ValidationError):
        validator(value)

def test_regex_validator_call_invert_match():
    validator = RegexValidator(regex=r'^\d+$', message='Invalid input', code='invalid', inverse_match=True)
    valid_value = 'abc123'
    try:
        validator(valid_value)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly")

    invalid_value = '123456'
    with pytest.raises(ValidationError):
        validator(invalid_value)