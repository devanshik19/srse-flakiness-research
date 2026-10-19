import pytest
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def test_regex_validator_call():
    # Test valid input matching the regex
    validator = RegexValidator(regex=r'^\d+$', message='Only digits are allowed', code='invalid')
    try:
        validator('12345')  # Should not raise an error
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for valid input.")

    # Test valid input not matching the regex when inverse_match is True
    validator_inverse = RegexValidator(regex=r'^\d+$', inverse_match=True, message='Only digits are allowed', code='invalid')
    try:
        validator_inverse('abc')  # Should not raise an error
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for valid input not matching when inverse_match is True.")

    # Test invalid input not matching regex
    with pytest.raises(ValidationError) as exc_info:
        validator('abc')  # Should raise ValidationError
    assert str(exc_info.value) == 'Only digits are allowed'

    # Test invalid input matching regex when inverse_match is True
    with pytest.raises(ValidationError) as exc_info:
        validator_inverse('12345')  # Should raise ValidationError
    assert str(exc_info.value) == 'Only digits are allowed'