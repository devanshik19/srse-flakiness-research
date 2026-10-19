import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

def test_regex_validator_valid():
    # Test with a valid input for default regex
    validator = RegexValidator(regex=r'^\w+@\w+\.\w+$', message='Invalid email format')
    try:
        validator('test@example.com')  # Should not raise
    except ValidationError:
        pytest.fail("ValidationError raised for valid input")

def test_regex_validator_invalid():
    # Test with an invalid input for default regex
    validator = RegexValidator(regex=r'^\w+@\w+\.\w+$', message='Invalid email format')
    with pytest.raises(ValidationError) as excinfo:
        validator('invalid_email')
    assert str(excinfo.value) == 'Invalid email format'

def test_regex_validator_inverse_match_valid():
    # Test with an input that should not match the regex (inverse_match=True)
    validator = RegexValidator(regex=r'^\w+@\w+\.\w+$', message='Invalid email format', inverse_match=True)
    try:
        validator('invalid_email')  # Should not raise
    except ValidationError:
        pytest.fail("ValidationError raised for valid input")

def test_regex_validator_inverse_match_invalid():
    # Test with an input that should match the regex (inverse_match=True)
    validator = RegexValidator(regex=r'^\w+@\w+\.\w+$', message='Invalid email format', inverse_match=True)
    with pytest.raises(ValidationError) as excinfo:
        validator('test@example.com')
    assert str(excinfo.value) == 'Invalid email format'