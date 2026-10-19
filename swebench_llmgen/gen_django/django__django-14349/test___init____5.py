import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def test_regex_validator_init():
    # Test with only regex provided
    validator = RegexValidator(regex=r'^\d+$')
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with regex and message
    validator = RegexValidator(regex=r'^\d+$', message='Must be a number')
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be a number'

    # Test with all parameters
    validator = RegexValidator(regex=r'^[a-zA-Z]+$', message='Must be letters', code='invalid', inverse_match=False, flags='IGNORECASE')
    assert validator.regex.pattern == r'^[a-zA-Z]+$'
    assert validator.message == 'Must be letters'
    assert validator.code == 'invalid'
    assert validator.inverse_match is False
    assert validator.flags == 'IGNORECASE'

    # Test with invalid flags (not a string)
    with pytest.raises(TypeError, match="If the flags are set, regex must be a regular expression string."):
        RegexValidator(regex=123, flags='IGNORECASE')

    # Test with flags and no regex
    with pytest.raises(TypeError, match="If the flags are set, regex must be a regular expression string."):
        RegexValidator(flags='IGNORECASE')