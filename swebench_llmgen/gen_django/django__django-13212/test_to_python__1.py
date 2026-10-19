import pytest
from django.forms.fields import Field

class TestField:
    @pytest.fixture
    def field_instance(self):
        return Field()

    def test_to_python_with_none(self, field_instance):
        assert field_instance.to_python(None) is None

    def test_to_python_with_string(self, field_instance):
        assert field_instance.to_python("test string") == "test string"

    def test_to_python_with_integer(self, field_instance):
        assert field_instance.to_python(123) == 123

    def test_to_python_with_float(self, field_instance):
        assert field_instance.to_python(123.45) == 123.45

    def test_to_python_with_decimal(self, field_instance):
        from decimal import Decimal
        assert field_instance.to_python(Decimal('123.45')) == Decimal('123.45')

    def test_to_python_with_boolean(self, field_instance):
        assert field_instance.to_python(True) is True
        assert field_instance.to_python(False) is False

    def test_to_python_with_list(self, field_instance):
        assert field_instance.to_python([1, 2, 3]) == [1, 2, 3]

    def test_to_python_with_dict(self, field_instance):
        assert field_instance.to_python({'key': 'value'}) == {'key': 'value'}