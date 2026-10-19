import pytest
from django.core.validators import RegexValidator

def test_regex_validator_init():
    # Test with all arguments provided
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='invalid_digits', inverse_match=False, flags=0)
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'invalid_digits'
    assert validator.inverse_match is False
    assert validator.flags == 0

    # Test with only regex
    validator = RegexValidator(regex=r'^[a-z]+$')
    assert validator.regex.pattern == r'^[a-z]+$'
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with invalid flags type
    with pytest.raises(TypeError):
        RegexValidator(regex=123, flags=0)

    # Test with None regex and some flags
    with pytest.raises(TypeError):
        RegexValidator(flags=0)

    # Test with default parameters
    validator = RegexValidator()
    assert validator.regex.pattern is None
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None