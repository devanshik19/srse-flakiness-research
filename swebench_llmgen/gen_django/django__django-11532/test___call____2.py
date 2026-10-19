import pytest
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

@pytest.fixture
def regex_validator():
    return RegexValidator(regex=re.compile(r'^\d+$'), message='Must be a number.', code='invalid')

def test_regex_validator_valid_input(regex_validator):
    # Test with a valid number
    regex_validator('1234')  # Should not raise ValidationError

def test_regex_validator_invalid_input(regex_validator):
    # Test with an invalid string that does not match the regex
    with pytest.raises(ValidationError, match='Must be a number.'):
        regex_validator('abc')

def test_regex_validator_invalid_input_with_inverse_match():
    # Test with inverse_match
    validator = RegexValidator(regex=re.compile(r'^\d+$'), inverse_match=True, message='Must not be a number.', code='invalid')
    
    # Test with an input that matches the regex (should raise)
    with pytest.raises(ValidationError, match='Must not be a number.'):
        validator('1234')

    # Test with an input that does not match the regex (should not raise)
    validator('abc')  # Should not raise ValidationError