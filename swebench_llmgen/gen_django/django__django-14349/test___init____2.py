import pytest
from django.core.validators import RegexValidator

def test_regex_validator_initialization():
    # Test valid initialization
    validator = RegexValidator(regex=r'^\d{3}-\d{2}-\d{4}$', message='Invalid format', code='invalid')
    assert validator.regex.pattern == r'^\d{3}-\d{2}-\d{4}$'
    assert validator.message == 'Invalid format'
    assert validator.code == 'invalid'
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test initialization with inverse_match
    validator = RegexValidator(regex=r'^\d{3}-\d{2}-\d{4}$', inverse_match=True)
    assert validator.inverse_match is True

    # Test initialization with flags
    validator = RegexValidator(regex=r'^\d{3}-\d{2}-\d{4}$', flags='i')
    assert validator.flags == 'i'

    # Test TypeError when flags are set and regex is not a string
    with pytest.raises(TypeError, match="If the flags are set, regex must be a regular expression string."):
        RegexValidator(regex=123, flags='i')

    # Test setting regex to None
    validator = RegexValidator()
    assert validator.regex is None