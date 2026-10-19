import pytest
from django.forms.fields import Field

class TestField:
    def test_to_python_with_valid_value(self):
        field = Field()
        assert field.to_python('valid input') == 'valid input'

    def test_to_python_with_none_value(self):
        field = Field()
        assert field.to_python(None) is None

    def test_to_python_with_integer_value(self):
        field = Field()
        assert field.to_python(123) == 123

    def test_to_python_with_float_value(self):
        field = Field()
        assert field.to_python(123.456) == 123.456

    def test_to_python_with_decimal_value(self):
        from decimal import Decimal
        field = Field()
        assert field.to_python(Decimal('123.456')) == Decimal('123.456')

    def test_to_python_with_empty_string(self):
        field = Field()
        assert field.to_python('') == ''

    def test_to_python_with_boolean_value(self):
        field = Field()
        assert field.to_python(True) is True
        assert field.to_python(False) is False