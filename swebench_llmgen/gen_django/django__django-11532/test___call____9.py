import pytest
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

@pytest.mark.parametrize("value, should_raise", [
    ("valid_string", False),    # should match the regex
    ("INVALID_STRING", True),    # should not match the regex
    ("12345", False),            # should match the regex
    ("abcdef", True),            # should not match the regex
])
def test_regex_validator(value, should_raise):
    regex = re.compile(r'[0-9]+')  # Regex to match any numbers
    validator = RegexValidator(regex=regex, message="Invalid input.", code="invalid")

    if should_raise:
        with pytest.raises(ValidationError):
            validator(value)
    else:
        validator(value)

def test_regex_validator_inverse_match():
    regex = re.compile(r'[0-9]+')
    validator = RegexValidator(regex=regex, inverse_match=True, message="Input should not match.", code="match_found")

    # Test should raise the ValidationError
    with pytest.raises(ValidationError):
        validator("12345")  # Matches the regex

    # Test should pass without exception
    validator("abcdef")  # Does not match the regex