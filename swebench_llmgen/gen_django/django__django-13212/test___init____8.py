import pytest
import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def test_regex_validator_init():
    # Test with valid parameters
    validator = RegexValidator(regex=r'^\d+$', message='Must be a number', code='invalid')
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be a number'
    assert validator.code == 'invalid'
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with inverse_match
    validator = RegexValidator(regex=r'^\d+$', message='Must be a number', inverse_match=True)
    assert validator.inverse_match is True

    # Test with flags
    validator = RegexValidator(regex=r'^\d+$', message='Must be a number', flags=re.IGNORECASE)
    assert validator.flags == re.IGNORECASE

    # Test with invalid regex type
    with pytest.raises(TypeError):
        RegexValidator(regex=123, flags=re.IGNORECASE)

    # Test with valid regex and flags
    validator = RegexValidator(regex='^[a-zA-Z]+$', flags=re.IGNORECASE)
    assert validator.regex.pattern == '^[a-zA-Z]+$'