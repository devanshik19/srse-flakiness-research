import pytest
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

def test_regex_validator():
    # Valid regex
    regex = re.compile(r'^\w+$')  # Matches any string with word characters
    message = "Invalid input."
    code = "invalid"
    
    # Instantiate the RegexValidator
    validator = RegexValidator(regex=regex, message=message, code=code, inverse_match=False)

    # Test valid inputs
    assert validator("validInput123") == None
    assert validator("anotherValidInput") == None

    # Test invalid inputs
    with pytest.raises(ValidationError) as excinfo:
        validator("invalid input!")  # Contains whitespace and non-word characters

    assert excinfo.value.message == message
    assert excinfo.value.code == code

    # Test inverse match
    inverse_validator = RegexValidator(regex=regex, message=message, code=code, inverse_match=True)

    # Test valid inputs with inverse match
    assert inverse_validator("invalid input!") == None

    # Test invalid inputs with inverse match
    with pytest.raises(ValidationError) as excinfo:
        inverse_validator("validInput123")  # Should raise because it matches the regex

    assert excinfo.value.message == message
    assert excinfo.value.code == code