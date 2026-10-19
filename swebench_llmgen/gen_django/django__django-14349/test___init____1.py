import pytest
from django.core.validators import RegexValidator


def test_regex_validator_init_with_valid_params():
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='invalid', inverse_match=False, flags=0)
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'invalid'
    assert validator.inverse_match is False
    assert validator.flags == 0


def test_regex_validator_init_with_none_params():
    validator = RegexValidator()
    assert validator.regex.pattern == ''
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None


def test_regex_validator_init_with_invalid_flags():
    with pytest.raises(TypeError, match="If the flags are set, regex must be a regular expression string."):
        RegexValidator(regex=123, flags=re.IGNORECASE)


def test_regex_validator_init_with_message_and_code():
    validator = RegexValidator(regex=r'^[a-zA-Z]+$', message='Only letters', code='letters_only')
    assert validator.message == 'Only letters'
    assert validator.code == 'letters_only'