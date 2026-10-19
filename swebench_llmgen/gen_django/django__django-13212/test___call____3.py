import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def test_regex_validator_call():
    # Test valid input without inverse_match
    validator = RegexValidator(regex=r'^[A-Za-z0-9]*$', message='Invalid input', code='invalid')
    
    # Should not raise ValidationError for valid input
    try:
        validator('ValidInput123')
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for valid input")

    # Test invalid input without inverse_match
    with pytest.raises(ValidationError) as excinfo:
        validator('Invalid Input!')
    assert str(excinfo.value) == 'Invalid input'

    # Test valid input with inverse_match
    validator_inverse = RegexValidator(regex=r'^[A-Za-z0-9]*$', inverse_match=True, message='Invalid input', code='invalid')

    # Should raise ValidationError for valid input since inverse_match is True
    with pytest.raises(ValidationError) as excinfo:
        validator_inverse('ValidInput123')
    assert str(excinfo.value) == 'Invalid input'

    # Test invalid input with inverse_match
    try:
        validator_inverse('Invalid Input!')
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for invalid input with inverse_match")