import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def test_regex_validator_init():
    # Test with all parameters
    validator = RegexValidator(regex='^[a-z]+$', message='Invalid input', code='invalid', inverse_match=False, flags=None)
    assert validator.regex.pattern == '^[a-z]+$'
    assert validator.message == 'Invalid input'
    assert validator.code == 'invalid'
    assert validator.inverse_match is False
    assert validator.flags is None

    # Test with only regex
    validator = RegexValidator(regex='^\d+$')
    assert validator.regex.pattern == '^\d+$' 

    # Test invalid flags with non-string regex
    with pytest.raises(TypeError) as excinfo:
        RegexValidator(regex=123, flags=re.IGNORECASE)
    assert str(excinfo.value) == 'If the flags are set, regex must be a regular expression string.'

    # Test with None values
    validator = RegexValidator()
    assert validator.regex.pattern == ''
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None