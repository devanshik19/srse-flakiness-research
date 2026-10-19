import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.fields import Field

class CustomField(Field):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        return super().to_python(value)

def test_to_python_with_valid_value():
    field = CustomField()
    valid_value = 'valid_string'
    result = field.to_python(valid_value)
    assert result == valid_value

def test_to_python_with_empty_value():
    field = CustomField()
    field.empty_values = [None, '']
    result = field.to_python('')
    assert result is None

def test_to_python_with_invalid_type():
    field = CustomField()
    with pytest.raises(ValidationError):
        field.to_python(object())