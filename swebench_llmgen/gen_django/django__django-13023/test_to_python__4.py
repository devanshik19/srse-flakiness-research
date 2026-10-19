import pytest
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

class Field:
    def to_python(self, value):
        """
        Convert the input value into the expected Python data type, raising
        django.core.exceptions.ValidationError if the data can't be converted.
        Return the converted value. Subclasses should override this.
        """
        return value

def test_to_python_with_valid_value():
    field = Field()
    assert field.to_python('test_value') == 'test_value'

def test_to_python_with_integer_value():
    field = Field()
    assert field.to_python(123) == 123

def test_to_python_with_none_value():
    field = Field()
    assert field.to_python(None) is None

def test_to_python_with_boolean_value():
    field = Field()
    assert field.to_python(True) is True
    assert field.to_python(False) is False

def test_to_python_with_empty_string():
    field = Field()
    assert field.to_python('') == ''

def test_to_python_with_invalid_value():
    field = Field()
    with pytest.raises(ValidationError):
        field.to_python(object())