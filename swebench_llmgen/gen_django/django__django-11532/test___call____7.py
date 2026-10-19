import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

@pytest.mark.parametrize("value, should_raise", [
    ("valid123", False),   # Should pass
    ("invalid@", True),    # Should raise ValidationError
    ("test", False),       # Should pass
    ("1234", True),        # Should raise ValidationError if inverse_match is True
])
def test_regex_validator(value, should_raise):
    validator = RegexValidator(regex=r'^[a-zA-Z0-9]+$', message="Invalid input", code="invalid")
    
    if should_raise:
        with pytest.raises(ValidationError):
            validator(value)
    else:
        try:
            validator(value)
        except ValidationError:
            pytest.fail("ValidationError was raised unexpectedly.")

@pytest.mark.parametrize("value, inverse_match, should_raise", [
    ("valid123", True, True),  # Should raise ValidationError
    ("invalid@", True, False),  # Should pass
])
def test_regex_validator_inverse(value, inverse_match, should_raise):
    validator = RegexValidator(regex=r'^[a-zA-Z0-9]+$', message="Invalid input", code="invalid", inverse_match=inverse_match)
    
    if should_raise:
        with pytest.raises(ValidationError):
            validator(value)
    else:
        try:
            validator(value)
        except ValidationError:
            pytest.fail("ValidationError was raised unexpectedly.")