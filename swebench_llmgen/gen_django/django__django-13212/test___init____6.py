import pytest
from django.core.validators import RegexValidator

def test_regex_validator_init_valid():
    validator = RegexValidator(regex=r'^\d+$', message='Must be a number', code='invalid')

    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be a number'
    assert validator.code == 'invalid'
    assert validator.inverse_match is None
    assert validator.flags is None

def test_regex_validator_init_with_inverse_match():
    validator = RegexValidator(regex=r'^\d+$', inverse_match=True)

    assert validator.regex.pattern == r'^\d+$'
    assert validator.inverse_match is True

def test_regex_validator_init_with_flags():
    with pytest.raises(TypeError, match="If the flags are set, regex must be a regular expression string."):
        RegexValidator(regex=None, flags=re.IGNORECASE)

    validator = RegexValidator(regex=r'^\s*$', flags=re.IGNORECASE)
    assert validator.regex.pattern == r'^\s*$'
    assert validator.flags == re.IGNORECASE

def test_regex_validator_init_no_regex():
    validator = RegexValidator()

    assert validator.regex is None
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None