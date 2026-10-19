import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

class TestField(models.Field):
    def to_python(self, value):
        super().to_python(value)
        if value is None:
            return None
        if isinstance(value, str) and value.isdigit():
            return int(value)
        raise ValidationError('Invalid value.')

def test_to_python_valid_string_numbers():
    field = TestField()
    assert field.to_python('123') == 123

def test_to_python_valid_none():
    field = TestField()
    assert field.to_python(None) is None

def test_to_python_invalid_string():
    field = TestField()
    with pytest.raises(ValidationError):
        field.to_python('abc')

def test_to_python_invalid_number():
    field = TestField()
    with pytest.raises(ValidationError):
        field.to_python([])

def test_to_python_valid_integer():
    field = TestField()
    assert field.to_python(456) == 456