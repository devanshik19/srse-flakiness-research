import pytest
from django.core.validators import RegexValidator

def test_regex_validator_init():
    # Test with default parameters
    validator = RegexValidator()
    assert validator.regex is not None
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with a valid regex and options
    validator = RegexValidator(regex='[a-z]+', message='Must be lowercase', code='invalid')
    assert validator.regex.pattern == '[a-z]+'
    assert validator.message == 'Must be lowercase'
    assert validator.code == 'invalid'

    # Test with flags
    validator = RegexValidator(regex='[A-Z]+', flags=re.IGNORECASE)
    assert validator.regex.pattern == '[A-Z]+'
    assert validator.flags == re.IGNORECASE

    # Test with inverse_match
    validator = RegexValidator(regex='[0-9]+', inverse_match=True)
    assert validator.inverse_match is True

    # Test raising TypeError if flags are set but regex is not a string
    with pytest.raises(TypeError):
        RegexValidator(flags=re.IGNORECASE, regex=123)

    # Test raising TypeError if flags are set but regex is None
    with pytest.raises(TypeError):
        RegexValidator(flags=re.IGNORECASE)

    # Test initializing with None regex, should not raise
    validator = RegexValidator(regex=None)
    assert validator.regex is not None  # Should be a compiled pattern even if regex is None