import pytest
import re
from django.core.validators import RegexValidator


def test_regex_validator_init_with_valid_regex():
    validator = RegexValidator(regex=r'^\w+$', message='Invalid input')
    assert isinstance(validator.regex, re.Pattern)
    assert validator.message == 'Invalid input'
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None


def test_regex_validator_init_with_flags():
    validator = RegexValidator(regex=r'^\d+$', flags=re.IGNORECASE)
    assert isinstance(validator.regex, re.Pattern)
    assert validator.flags == re.IGNORECASE


def test_regex_validator_init_with_inverse_match():
    validator = RegexValidator(regex=r'foo', inverse_match=True)
    assert validator.inverse_match is True


def test_regex_validator_init_raises_type_error_if_flags_set_without_string_regex():
    with pytest.raises(TypeError):
        RegexValidator(regex=123, flags=re.IGNORECASE)