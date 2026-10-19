import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def test_regex_validator_init():
    # Test with all parameters
    validator = RegexValidator(regex='^\\d+$', message='Must be digits', code='invalid', inverse_match=False, flags=None)
    assert validator.regex.pattern == '^\\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'invalid'
    assert validator.inverse_match is False
    assert validator.flags is None

    # Test with regex only
    validator = RegexValidator(regex='^[a-z]+$')
    assert validator.regex.pattern == '^[a-z]+$'
    
    # Test with message
    validator = RegexValidator(regex='^\\w+$', message='Must be alphanumeric')
    assert validator.message == 'Must be alphanumeric'

    # Test with code
    validator = RegexValidator(regex='^\\s*$', code='blank')
    assert validator.code == 'blank'

    # Test with flags and check TypeError
    with pytest.raises(TypeError):
        RegexValidator(regex=['a', 'b'], flags=1)

    # Test with valid flags
    validator = RegexValidator(regex='^(?i)abc$', flags=re.IGNORECASE)
    assert validator.regex.pattern == '^(?i)abc$'