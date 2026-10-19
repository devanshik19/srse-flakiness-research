import pytest
from django.core.validators import RegexValidator

def test_regex_validator_init():
    # Test with all parameters provided
    validator = RegexValidator(regex=r'^\d+$', message='Must be a number', code='invalid', inverse_match=False, flags=None)
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be a number'
    assert validator.code == 'invalid'
    assert validator.inverse_match is False
    assert validator.flags is None

    # Test with only regex
    validator = RegexValidator(regex=r'^[a-zA-Z]+$')
    assert validator.regex.pattern == r'^[a-zA-Z]+$'
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with regex and message
    validator = RegexValidator(regex=r'^\w+$', message='Only word characters allowed')
    assert validator.regex.pattern == r'^\w+$'
    assert validator.message == 'Only word characters allowed'

    # Test invalid flag type raises TypeError
    with pytest.raises(TypeError):
        RegexValidator(regex=123, flags=0)

    # Test valid flag with string regex
    validator = RegexValidator(regex=r'^[0-9]+$', flags=re.IGNORECASE)
    assert validator.regex.pattern == r'^[0-9]+$'