import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

def test_regex_validator():
    # Define test cases
    valid_cases = [
        ("valid123", False),
        ("123valid", False),
        ("valid", False)
    ]
    
    invalid_cases = [
        ("invalid!", False),
        ("123invalid", True),
        ("another_invalid#", True)
    ]
    
    # Test the RegexValidator with direct regex
    regex_validator = RegexValidator(regex=r'^[A-Za-z0-9]*$', message="Invalid input", code="invalid")

    # Test valid inputs
    for value, inverse in valid_cases:
        try:
            regex_validator(value)
        except ValidationError:
            pytest.fail(f"ValidationError raised unexpectedly for valid input: '{value}'")

    # Test invalid inputs
    for value, inverse in invalid_cases:
        if not inverse:
            with pytest.raises(ValidationError, match="Invalid input"):
                regex_validator(value)
        else:
            regex_validator.inverse_match = True
            with pytest.raises(ValidationError, match="Invalid input"):
                regex_validator(value)