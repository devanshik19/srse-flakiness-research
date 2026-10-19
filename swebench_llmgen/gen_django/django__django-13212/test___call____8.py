import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

def test_regex_validator_call():
    # Test parameters
    regex = r'^\d{3}-\d{2}-\d{4}$'  # Example regex for matching a specific format (SSN)
    message = "Invalid format"
    code = "invalid_format"
    
    # Create the RegexValidator instance
    validator = RegexValidator(regex=regex, message=message, code=code, inverse_match=False)
    
    # Test with valid input
    valid_value = '123-45-6789'
    try:
        validator(valid_value)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for valid input.")
    
    # Test with invalid input
    invalid_value = '123-456-789'
    with pytest.raises(ValidationError) as excinfo:
        validator(invalid_value)
    assert excinfo.value.message == message
    assert excinfo.value.code == code

    # Test with inverse match
    inverse_validator = RegexValidator(regex=regex, message=message, code=code, inverse_match=True)
    
    # Test with valid input should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        inverse_validator(valid_value)
    assert excinfo.value.message == message
    assert excinfo.value.code == code
    
    # Test with invalid input (which is valid according to inverse)
    try:
        inverse_validator(invalid_value)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for invalid input with inverse match.")