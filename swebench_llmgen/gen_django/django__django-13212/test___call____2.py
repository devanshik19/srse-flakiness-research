import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

def test_regex_validator_call():
    # Create a RegexValidator instance for testing
    regex_validator = RegexValidator(regex=r'^\d+$', message='Must be digits.', code='invalid')

    # Test with valid input
    valid_input = '123456'
    try:
        regex_validator(valid_input)  # Should not raise ValidationError
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for valid input.")

    # Test with invalid input
    invalid_input = '123a456'
    with pytest.raises(ValidationError) as excinfo:
        regex_validator(invalid_input)
    assert str(excinfo.value) == 'Must be digits.'

    # Test with inverse_match
    inverse_validator = RegexValidator(regex=r'^\d+$', inverse_match=True, message='Must not be digits.', code='invalid')
    
    # Test with invalid input for inverse_match
    with pytest.raises(ValidationError) as excinfo:
        inverse_validator(valid_input)
    assert str(excinfo.value) == 'Must not be digits.'

    # Test with valid input for inverse_match
    try:
        inverse_validator(invalid_input)  # Should not raise ValidationError
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for valid input with inverse_match.")