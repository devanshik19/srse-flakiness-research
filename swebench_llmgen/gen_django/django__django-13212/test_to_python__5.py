import pytest
from django.forms import Field

class TestField:

    @pytest.fixture
    def field_instance(self):
        return Field()

    def test_to_python_with_none(self, field_instance):
        assert field_instance.to_python(None) is None

    def test_to_python_with_string(self, field_instance):
        value = "test string"
        assert field_instance.to_python(value) == value

    def test_to_python_with_integer(self, field_instance):
        value = 123
        assert field_instance.to_python(value) == value

    def test_to_python_with_float(self, field_instance):
        value = 123.456
        assert field_instance.to_python(value) == value

    def test_to_python_with_boolean(self, field_instance):
        value = True
        assert field_instance.to_python(value) == value

    def test_to_python_with_list(self, field_instance):
        value = [1, 2, 3]
        assert field_instance.to_python(value) == value

    def test_to_python_with_dict(self, field_instance):
        value = {'key': 'value'}
        assert field_instance.to_python(value) == value