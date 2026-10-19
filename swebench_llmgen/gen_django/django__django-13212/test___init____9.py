import pytest
from django.core.validators import RegexValidator

def test_regex_validator_initialization():
    # Test with all parameters provided
    validator = RegexValidator(regex=r'^\d+$', message='Must be digits', code='invalid', inverse_match=False, flags=0)
    assert validator.regex.pattern == r'^\d+$'
    assert validator.message == 'Must be digits'
    assert validator.code == 'invalid'
    assert validator.inverse_match is False
    assert validator.flags == 0

    # Test with only regex provided
    validator = RegexValidator(regex=r'^[a-z]*$')
    assert validator.regex.pattern == r'^[a-z]*$'
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None

    # Test when flags are set without regex
    with pytest.raises(TypeError):
        RegexValidator(flags=0)

    # Test invalid regex string raises appropriate error
    with pytest.raises(re.error):
        RegexValidator(regex='[a-z')

    # Test with inverse_match set to True
    validator = RegexValidator(regex=r'^\d+$', inverse_match=True)
    assert validator.inverse_match is True

    # Test initialization with None values
    validator = RegexValidator()
    assert validator.regex is None
    assert validator.message is None
    assert validator.code is None
    assert validator.inverse_match is None
    assert validator.flags is None