import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def test_regex_validator_validates_correctly():
    # Valid regex case
    validator = RegexValidator(regex=r'^\d+$', message='Enter a number', code='invalid')
    
    # Test valid input
    try:
        validator('12345')
    except ValidationError:
        pytest.fail("ValidationError raised on valid input")

    # Test invalid input
    with pytest.raises(ValidationError) as exc_info:
        validator('abc')
    assert str(exc_info.value) == 'Enter a number'

def test_regex_validator_inverse_match():
    # Inverse match case
    validator = RegexValidator(regex=r'^\d+$', inverse_match=True, message='Should not be a number', code='invalid')

    # Test invalid input for inverse match
    try:
        validator('abc')
    except ValidationError:
        pytest.fail("ValidationError raised on invalid input for inverse match")

    # Test valid input for inverse match
    with pytest.raises(ValidationError) as exc_info:
        validator('12345')
    assert str(exc_info.value) == 'Should not be a number'