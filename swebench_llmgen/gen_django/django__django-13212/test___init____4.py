import pytest
from django.core.validators import RegexValidator

def test_regex_validator_init():
    # Test with all parameters set
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='digits_only', inverse_match=False, flags=0)
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'digits_only'
    assert validator.inverse_match is False
    assert validator.flags == 0

    # Test with only regex
    validator = RegexValidator(regex=r'^[a-z]+$')
    assert validator.regex.pattern == r'^[a-z]+$'
    
    # Test with message
    validator = RegexValidator(regex=r'^\w+$', message='Must be alphanumeric')
    assert validator.message == 'Must be alphanumeric'
    
    # Test with code
    validator = RegexValidator(regex=r'^\S+$', code='no_spaces')
    assert validator.code == 'no_spaces'
    
    # Test with inverse_match
    validator = RegexValidator(regex=r'^[A-Z]+$', inverse_match=True)
    assert validator.inverse_match is True
    
    # Test with flags
    validator = RegexValidator(regex=r'^\d+$', flags=re.IGNORECASE)
    assert validator.flags == re.IGNORECASE

    # Test invalid case for flags and non-string regex
    with pytest.raises(TypeError):
        RegexValidator(regex=123, flags=re.IGNORECASE)