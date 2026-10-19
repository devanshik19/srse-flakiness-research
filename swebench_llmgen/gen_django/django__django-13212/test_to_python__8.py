import pytest
from django.forms.fields import Field

class TestField:
    @pytest.fixture
    def field(self):
        return Field()

    def test_to_python_returns_same_value(self, field):
        assert field.to_python('test_value') == 'test_value'
        assert field.to_python(123) == 123
        assert field.to_python(None) is None
        assert field.to_python(True) is True
        assert field.to_python([1, 2, 3]) == [1, 2, 3]
        assert field.to_python({ 'key': 'value' }) == { 'key': 'value' }