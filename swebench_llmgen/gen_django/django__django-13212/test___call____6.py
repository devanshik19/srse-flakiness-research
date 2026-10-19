import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

def test_regex_validator():
    # Test case: Valid value when inverse_match is False
    validator = RegexValidator(regex=r'^\d{3}-\d{2}-\d{4}$', message='Invalid format', code='invalid')
    try:
        validator('123-45-6789')  # Should not raise
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for valid input.")

    # Test case: Invalid value when inverse_match is False
    with pytest.raises(ValidationError) as exc_info:
        validator('123-45')  # Should raise ValidationError
    assert str(exc_info.value) == 'Invalid format'

    # Test case: Valid value when inverse_match is True
    validator_inverse = RegexValidator(regex=r'^\d{3}-\d{2}-\d{4}$', inverse_match=True, message='Invalid format', code='invalid')
    try:
        validator_inverse('123-45')  # Should not raise
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for valid input.")

    # Test case: Invalid value when inverse_match is True
    with pytest.raises(ValidationError) as exc_info:
        validator_inverse('123-45-6789')  # Should raise ValidationError
    assert str(exc_info.value) == 'Invalid format'

    # Test case: Edge case with empty string
    try:
        validator('')  # Should not raise
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for empty input.")

    # Test case: Edge case with None
    try:
        validator(None)  # Should not raise
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for None input.")