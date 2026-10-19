import pytest
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class TestRegexValidator:
    def setup_method(self):
        self.regex = re.compile(r'^\d{3}-\d{2}-\d{4}$')  # Example pattern: XXX-XX-XXXX
        self.message = "Invalid format"
        self.code = "invalid"
        self.validator = RegexValidator(self.regex, self.message, self.code)

    def test_valid_input(self):
        valid_value = '123-45-6789'
        try:
            self.validator(valid_value)
        except ValidationError:
            pytest.fail("ValidationError raised for valid input")

    def test_invalid_input(self):
        invalid_value = '123-456-789'
        with pytest.raises(ValidationError) as excinfo:
            self.validator(invalid_value)
        assert excinfo.value.code == self.code

    def test_invalid_format_due_to_inverse_match(self):
        self.validator.inverse_match = True
        valid_value = '123-45-6789'
        with pytest.raises(ValidationError) as excinfo:
            self.validator(valid_value)
        assert excinfo.value.code == self.code

    def test_valid_format_due_to_inverse_match(self):
        self.validator.inverse_match = True
        invalid_value = '123-456-789'
        try:
            self.validator(invalid_value)
        except ValidationError:
            pytest.fail("ValidationError raised for valid input with inverse match")