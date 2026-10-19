import pytest
from django.core.validators import RegexValidator

def test_regex_validator_init():
    # Test with all parameters
    validator = RegexValidator(regex=r'^[a-zA-Z0-9_]+$', message='Invalid', code='invalid', inverse_match=False, flags=0)
    assert validator.regex.pattern == r'^[a-zA-Z0-9_]+$'
    assert validator.message == 'Invalid'
    assert validator.code == 'invalid'
    assert validator.inverse_match is False
    assert validator.flags == 0

    # Test with only regex
    validator = RegexValidator(regex=r'^[\d]+$')
    assert validator.regex.pattern == r'^[\d]+$'
    
    # Test with no regex but passing other parameters
    validator = RegexValidator(message='Invalid format', code='invalid')
    assert validator.message == 'Invalid format'
    assert validator.regex is not None  # Should still compile to a default regex

    # Test with invalid flags
    with pytest.raises(TypeError):
        RegexValidator(regex=['invalid'], flags=0)

    # Test with None values
    validator = RegexValidator()
    assert validator.regex is not None  # Should compile to a default regex
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None