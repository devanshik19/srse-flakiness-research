import pytest
from django.forms.fields import Field

class TestField:
    def setup_method(self):
        self.field = Field()

    def test_to_python_with_string(self):
        value = "test string"
        assert self.field.to_python(value) == value

    def test_to_python_with_integer(self):
        value = 123
        assert self.field.to_python(value) == value

    def test_to_python_with_float(self):
        value = 123.45
        assert self.field.to_python(value) == value

    def test_to_python_with_none(self):
        value = None
        assert self.field.to_python(value) == value

    def test_to_python_with_empty_string(self):
        value = ""
        assert self.field.to_python(value) == value

    def test_to_python_with_list(self):
        value = [1, 2, 3]
        assert self.field.to_python(value) == value

    def test_to_python_with_dict(self):
        value = {"key": "value"}
        assert self.field.to_python(value) == value