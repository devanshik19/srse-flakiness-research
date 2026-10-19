import pytest
from django.forms.fields import Field

class TestField:
    @pytest.fixture
    def field_instance(self):
        return Field()

    def test_bound_data_with_disabled_field(self, field_instance):
        field_instance.disabled = True
        initial_data = 'Initial Data'
        submitted_data = 'Submitted Data'
        
        result = field_instance.bound_data(submitted_data, initial_data)
        
        assert result == initial_data

    def test_bound_data_with_enabled_field(self, field_instance):
        field_instance.disabled = False
        initial_data = 'Initial Data'
        submitted_data = 'Submitted Data'
        
        result = field_instance.bound_data(submitted_data, initial_data)
        
        assert result == submitted_data