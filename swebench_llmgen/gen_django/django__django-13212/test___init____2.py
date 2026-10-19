import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def test_regex_validator_init():
    # Test with all parameters set
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='invalid', inverse_match=False, flags=0)
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'invalid'
    assert validator.inverse_match is False
    assert validator.flags == 0

    # Test with only regex
    validator = RegexValidator(regex=r'^[a-z]+$')
    assert validator.regex.pattern == r'^[a-z]+$'
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test with message and code
    validator = RegexValidator(message='Invalid input', code='invalid')
    assert validator.message == 'Invalid input'
    assert validator.code == 'invalid'
    
    # Test invalid flags type
    with pytest.raises(TypeError):
        RegexValidator(regex=r'^[a-z]+$', flags=0.1)
    
    # Test with inverse_match
    validator = RegexValidator(regex=r'^[a-z]+$', inverse_match=True)
    assert validator.inverse_match is True

    # Test combination of parameters
    validator = RegexValidator(regex=r'^[A-Z]+$', message='All uppercase', code='uppercase', inverse_match=None, flags=None)
    assert validator.regex.pattern == r'^[A-Z]+$'
    assert validator.message == 'All uppercase'
    assert validator.code == 'uppercase'
    assert validator.inverse_match is None
    assert validator.flags is None