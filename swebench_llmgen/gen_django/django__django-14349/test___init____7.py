import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def test_regex_validator_init():
    # Test with valid parameters
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='invalid')
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'invalid'
    
    # Test with inverse match
    validator_inverse = RegexValidator(regex=r'^\d+$', inverse_match=True)
    assert validator_inverse.inverse_match is True
    
    # Test with flags
    validator_flags = RegexValidator(regex=r'^\d+$', flags=re.IGNORECASE)
    assert validator_flags.flags == re.IGNORECASE

    # Test without regex to check if TypeError is raised
    with pytest.raises(TypeError):
        RegexValidator(flags=re.IGNORECASE)

    # Test when flags are set but regex is not a string
    with pytest.raises(TypeError):
        RegexValidator(regex=123, flags=re.IGNORECASE)

    # Test creating a validator with all parameters
    validator_full = RegexValidator(regex=r'^[a-zA-Z]+$', message='Must be letters', code='invalid', inverse_match=False, flags=re.MULTILINE)
    assert validator_full.regex.pattern == r'^[a-zA-Z]+$'
    assert validator_full.message == 'Must be letters'
    assert validator_full.code == 'invalid'
    assert validator_full.inverse_match is False
    assert validator_full.flags == re.MULTILINE