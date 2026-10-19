import pytest
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class TestRegexValidator:

    def setup_method(self):
        self.valid_regex = re.compile(r'^[a-z]+$')
        self.invalid_regex = re.compile(r'^[0-9]+$')
        self.message = "Invalid input."
        self.code = "invalid"

    def test_call_valid_input(self):
        validator = RegexValidator(regex=self.valid_regex, message=self.message, code=self.code)

        # Test valid input
        try:
            validator("hello")
        except ValidationError:
            pytest.fail("ValidationError raised unexpectedly for valid input.")

    def test_call_invalid_input(self):
        validator = RegexValidator(regex=self.valid_regex, message=self.message, code=self.code)

        # Test invalid input
        with pytest.raises(ValidationError) as exc_info:
            validator("123")
        assert str(exc_info.value) == self.message
        assert exc_info.value.code == self.code

    def test_call_inverse_match(self):
        validator = RegexValidator(regex=self.valid_regex, message=self.message, code=self.code, inverse_match=True)

        # Test valid input when inverse_match is True (should raise validation error)
        with pytest.raises(ValidationError) as exc_info:
            validator("hello")
        assert str(exc_info.value) == self.message
        assert exc_info.value.code == self.code

        # Test invalid input when inverse_match is True (should not raise)
        try:
            validator("123")
        except ValidationError:
            pytest.fail("ValidationError raised unexpectedly for valid input with inverse_match.")