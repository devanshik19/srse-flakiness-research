import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def test_regex_validator_init_with_valid_regex():
    validator = RegexValidator(regex=r'^\d{3}-\d{2}-\d{4}$', message='Invalid format')
    assert validator.regex.pattern == r'^\d{3}-\d{2}-\d{4}$'
    assert validator.message == 'Invalid format'
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None

def test_regex_validator_init_with_no_regex():
    validator = RegexValidator()
    assert isinstance(validator.regex, type(re.compile('')))
    
def test_regex_validator_init_with_invalid_regex_type():
    with pytest.raises(TypeError, match="If the flags are set, regex must be a regular expression string."):
        RegexValidator(regex='not/a/regex', flags=re.IGNORECASE)

def test_regex_validator_init_with_all_parameters():
    validator = RegexValidator(regex=r'^[a-zA-Z0-9]+$', message='Only alphanumeric characters', code='invalid_chars', inverse_match=True, flags=re.IGNORECASE)
    assert validator.regex.pattern == r'^[a-zA-Z0-9]+$'
    assert validator.message == 'Only alphanumeric characters'
    assert validator.code == 'invalid_chars'
    assert validator.inverse_match is True
    assert validator.flags == re.IGNORECASE