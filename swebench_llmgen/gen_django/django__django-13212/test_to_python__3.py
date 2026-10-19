import pytest
from django.forms import Field

class TestField:

    @pytest.fixture
    def field_instance(self):
        return Field()

    def test_to_python_with_string(self, field_instance):
        value = "test_string"
        assert field_instance.to_python(value) == value

    def test_to_python_with_integer(self, field_instance):
        value = 123
        assert field_instance.to_python(value) == value

    def test_to_python_with_none(self, field_instance):
        value = None
        assert field_instance.to_python(value) == value

    def test_to_python_with_float(self, field_instance):
        value = 123.456
        assert field_instance.to_python(value) == value

    def test_to_python_with_empty_string(self, field_instance):
        value = ""
        assert field_instance.to_python(value) == value

    def test_to_python_with_boolean_true(self, field_instance):
        value = True
        assert field_instance.to_python(value) == value

    def test_to_python_with_boolean_false(self, field_instance):
        value = False
        assert field_instance.to_python(value) == value