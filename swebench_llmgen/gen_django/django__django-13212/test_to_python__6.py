import pytest
from django.forms.fields import Field

class TestField:

    def test_to_python_with_none(self):
        field = Field()
        assert field.to_python(None) is None

    def test_to_python_with_integer(self):
        field = Field()
        value = 5
        assert field.to_python(value) == value

    def test_to_python_with_string(self):
        field = Field()
        value = "test"
        assert field.to_python(value) == value

    def test_to_python_with_float(self):
        field = Field()
        value = 5.5
        assert field.to_python(value) == value

    def test_to_python_with_boolean(self):
        field = Field()
        value = True
        assert field.to_python(value) is True
        value = False
        assert field.to_python(value) is False

    def test_to_python_with_empty_string(self):
        field = Field()
        value = ""
        assert field.to_python(value) == value