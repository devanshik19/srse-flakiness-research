import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

@pytest.fixture
def validator():
    return RegexValidator(regex=r'^[a-zA-Z0-9]+$', message='Invalid input', code='invalid')

def test_regex_validator_valid_input(validator):
    # Test with valid input
    try:
        validator('ValidInput123')
    except ValidationError:
        pytest.fail("ValidationError raised on valid input")

def test_regex_validator_invalid_input(validator):
    # Test with invalid input
    with pytest.raises(ValidationError) as excinfo:
        validator('Invalid Input!')
    assert excinfo.value.message == 'Invalid input'
    assert excinfo.value.code == 'invalid'

def test_regex_validator_inverse_match(validator):
    # Test with inverse_match set to True
    inverse_validator = RegexValidator(regex=r'^[a-zA-Z0-9]+$', message='Invalid input', code='invalid', inverse_match=True)
    
    # Should raise ValidationError for valid input since it's inverse
    with pytest.raises(ValidationError) as excinfo:
        inverse_validator('ValidInput123')
    assert excinfo.value.message == 'Invalid input'
    assert excinfo.value.code == 'invalid'
    
    # Should not raise for invalid input
    try:
        inverse_validator('Invalid Input!')
    except ValidationError:
        pytest.fail("ValidationError raised on invalid input")