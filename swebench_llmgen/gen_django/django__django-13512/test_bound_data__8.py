import pytest
from django.forms.fields import Field

class TestField:

    @pytest.fixture
    def field(self):
        return Field()

    def test_bound_data_with_disabled_field(self, field):
        field.disabled = True
        initial_data = 'initial_value'
        bound_data = field.bound_data(None, initial_data)
        assert bound_data == initial_data

    def test_bound_data_with_enabled_field(self, field):
        field.disabled = False
        submitted_data = 'submitted_value'
        bound_data = field.bound_data(submitted_data, 'initial_value')
        assert bound_data == submitted_data

    def test_bound_data_with_none_data(self, field):
        field.disabled = False
        bound_data = field.bound_data(None, 'initial_value')
        assert bound_data is None