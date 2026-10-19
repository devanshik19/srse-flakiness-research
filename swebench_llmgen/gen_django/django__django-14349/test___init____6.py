import pytest
from django.core.validators import RegexValidator

def test_regex_validator_init():
    # Test with only the regex argument
    validator = RegexValidator(regex=r'^[a-z]+$')
    assert validator.regex.pattern == r'^[a-z]+$'
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with all arguments
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='digits_not_allowed', inverse_match=True, flags='i')
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'digits_not_allowed'
    assert validator.inverse_match is True
    assert validator.flags == 'i'

    # Test with invalid flags type
    with pytest.raises(TypeError, match="If the flags are set, regex must be a regular expression string."):
        RegexValidator(regex=123, flags='i')

    # Test with invalid regex when flags are present
    with pytest.raises(TypeError, match="If the flags are set, regex must be a regular expression string."):
        RegexValidator(flags='i')