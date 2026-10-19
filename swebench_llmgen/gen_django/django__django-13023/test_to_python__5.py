import pytest
from django.core.exceptions import ValidationError
from django.db.models.fields import Field

class CustomField(Field):
    def to_python(self, value):
        if value in (None, ''):
            return None
        if isinstance(value, str):
            return value.strip()
        raise ValidationError("Invalid value")

def test_to_python_with_none():
    field = CustomField()
    assert field.to_python(None) is None

def test_to_python_with_empty_string():
    field = CustomField()
    assert field.to_python('') is None

def test_to_python_with_string():
    field = CustomField()
    result = field.to_python('   some value   ')
    assert result == 'some value'

def test_to_python_with_invalid_type():
    field = CustomField()
    with pytest.raises(ValidationError, match="Invalid value"):
        field.to_python(123)

def test_to_python_with_extra_spaces():
    field = CustomField()
    result = field.to_python('   extra spaces   ')
    assert result == 'extra spaces'