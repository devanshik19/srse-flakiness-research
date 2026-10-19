import pytest
from django.core.validators import RegexValidator

def test_regex_validator_init():
    # Test with valid regex
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='invalid')
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'invalid'
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with inverse match
    validator = RegexValidator(regex=r'^\d+$', inverse_match=True)
    assert validator.inverse_match is True

    # Test with flags
    validator = RegexValidator(regex=r'^\d+$', flags=re.IGNORECASE)
    assert validator.flags == re.IGNORECASE

    # Test with invalid flags (not a string)
    with pytest.raises(TypeError):
        RegexValidator(regex=123, flags=re.IGNORECASE)

    # Test with no regex (should initialize without error)
    validator = RegexValidator()
    assert validator.regex is None
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None