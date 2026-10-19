import pytest
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

@pytest.mark.parametrize("value, expected_exception", [
    ("valid_value", None),
    ("invalid_value", ValidationError), # Assume invalid regex condition
])
def test_regex_validator_call(value, expected_exception):
    regex = r"^valid_.*$"  # Example regex that matches strings starting with "valid_"
    validator = RegexValidator(regex=regex, message="Invalid value", code="invalid")

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            validator(value)
        assert str(exc_info.value) == "Invalid value"  # Check if the raised error has the correct message
    else:
        validator(value)  # Should not raise an exception