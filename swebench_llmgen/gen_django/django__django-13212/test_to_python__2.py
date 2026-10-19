import pytest
from django.forms.fields import Field

class TestField:
    def test_to_python_with_string(self):
        field = Field()
        result = field.to_python("test string")
        assert result == "test string"

    def test_to_python_with_integer(self):
        field = Field()
        result = field.to_python(123)
        assert result == 123

    def test_to_python_with_float(self):
        field = Field()
        result = field.to_python(123.456)
        assert result == 123.456

    def test_to_python_with_none(self):
        field = Field()
        result = field.to_python(None)
        assert result is None

    def test_to_python_with_list(self):
        field = Field()
        result = field.to_python(['a', 'b', 'c'])
        assert result == ['a', 'b', 'c']

    def test_to_python_with_dict(self):
        field = Field()
        result = field.to_python({'key': 'value'})
        assert result == {'key': 'value'}

    def test_to_python_with_boolean(self):
        field = Field()
        result = field.to_python(True)
        assert result is True