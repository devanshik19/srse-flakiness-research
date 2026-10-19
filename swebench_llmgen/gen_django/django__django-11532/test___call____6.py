import pytest
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

@pytest.fixture
def regex_validator():
    return RegexValidator(regex=re.compile(r'^\d{3}-\d{2}-\d{4}$'), 
                           message='Value must be in the format XXX-XX-XXXX', 
                           code='invalid_format', 
                           inverse_match=False)

def test_regex_validator_valid_case(regex_validator):
    valid_value = '123-45-6789'
    try:
        regex_validator(valid_value)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly!")

def test_regex_validator_invalid_case(regex_validator):
    invalid_value = '123-456-789'
    with pytest.raises(ValidationError) as excinfo:
        regex_validator(invalid_value)
    assert excinfo.value.message == 'Value must be in the format XXX-XX-XXXX'
    assert excinfo.value.code == 'invalid_format'

def test_regex_validator_inverse_match(regex_validator):
    regex_validator.inverse_match = True
    invalid_value = '123-45-6789'
    with pytest.raises(ValidationError) as excinfo:
        regex_validator(invalid_value)
    assert excinfo.value.message == 'Value must be in the format XXX-XX-XXXX'
    assert excinfo.value.code == 'invalid_format'

    valid_value = '123-456-789'
    try:
        regex_validator(valid_value)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly!")