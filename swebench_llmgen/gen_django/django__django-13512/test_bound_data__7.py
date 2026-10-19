import pytest
from django.forms import Field

class TestField:

    @pytest.fixture
    def field_instance(self):
        # Create an instance of Field for testing
        return Field()

    def test_bound_data_with_disabled_field(self, field_instance):
        # Testing when the field is disabled
        field_instance.disabled = True
        initial_data = 'initial_value'
        result = field_instance.bound_data('submitted_value', initial_data)
        assert result == initial_data

    def test_bound_data_with_enabled_field(self, field_instance):
        # Testing when the field is enabled
        field_instance.disabled = False
        submitted_data = 'submitted_value'
        result = field_instance.bound_data(submitted_data, None)
        assert result == submitted_data

    def test_bound_data_with_none_initial(self, field_instance):
        # Testing when initial data is None
        field_instance.disabled = False
        result = field_instance.bound_data('submitted_value', None)
        assert result == 'submitted_value'