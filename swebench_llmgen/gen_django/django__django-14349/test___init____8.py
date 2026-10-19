import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def test_regex_validator_init():
    # Test with a valid regex
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='invalid')
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'invalid'
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with a regex and flags
    validator = RegexValidator(regex=r'^[a-zA-Z]+$', flags=re.IGNORECASE)
    assert validator.regex.pattern == r'^[a-zA-Z]+$'
    assert validator.flags == re.IGNORECASE

    # Test with an inverse match
    validator = RegexValidator(regex=r'^\d+$', inverse_match=True)
    assert validator.inverse_match is True

    # Test with a custom message
    validator = RegexValidator(regex=r'^\w+$', message='Only word characters allowed')
    assert validator.message == 'Only word characters allowed'

    # Test invalid flags with a non-string regex
    with pytest.raises(TypeError):
        RegexValidator(regex=[1, 2, 3], flags=re.IGNORECASE)

    # Test without providing any arguments
    validator = RegexValidator()
    assert validator.regex is None
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None