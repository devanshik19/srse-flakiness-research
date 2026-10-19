import pytest
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

def test_regex_validator():
    # Test case: Pattern matches, should not raise ValidationError
    validator = RegexValidator(regex=re.compile(r'^[a-zA-Z]+$'), message='Invalid input', code='invalid')
    
    try:
        validator("ValidInput")
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly!")

    # Test case: Pattern does not match, should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        validator("InvalidInput123")
    assert str(excinfo.value) == 'Invalid input'

    # Test case: Inverse match
    validator_inverse = RegexValidator(regex=re.compile(r'^[a-zA-Z]+$'), inverse_match=True, 
                                        message='Invalid input', code='invalid')
    
    # Should raise ValidationError since input matches the regex and inverse_match is True
    with pytest.raises(ValidationError) as excinfo:
        validator_inverse("ValidInput")
    assert str(excinfo.value) == 'Invalid input'

    # Should not raise ValidationError since input does not match the regex
    try:
        validator_inverse("123456")
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly for inverse match!")