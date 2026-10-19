import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Field


class TestField(Field):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        return super().to_python(value)


@pytest.mark.parametrize("input_value, expected_output", [
    (None, None),
    ("", None),
    ("valid_string", "valid_string"),
    (123, 123),
    (decimal.Decimal('123.45'), decimal.Decimal('123.45')),
    (uuid.uuid4(), uuid.uuid4()),  # Check for UUID handling
])
def test_to_python(input_value, expected_output):
    field = TestField()
    field.empty_values = [None, '']

    result = field.to_python(input_value)
    
    assert result == expected_output


def test_to_python_raises_validationerror():
    field = TestField()
    field.empty_values = [None, '']
    
    with pytest.raises(ValidationError):
        field.to_python(object())  # Passing an unsupported type