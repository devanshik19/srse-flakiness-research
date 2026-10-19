import pytest
from django.core.exceptions import ValidationError
from django.db.models import Field

class TestField(Field):
    def to_python(self, value):
        if value is None:
            return ''
        if isinstance(value, str):
            return value.strip()
        raise ValidationError("Invalid input type")

def test_to_python_with_string():
    field = TestField()
    assert field.to_python('  test_value  ') == 'test_value'

def test_to_python_with_none():
    field = TestField()
    assert field.to_python(None) == ''

def test_to_python_with_invalid_type():
    field = TestField()
    with pytest.raises(ValidationError, match="Invalid input type"):
        field.to_python(123)

def test_to_python_with_empty_string():
    field = TestField()
    assert field.to_python('') == ''