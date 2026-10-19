import pytest
from django.forms import Field
from django.contrib.auth.models import User

class TestField:

    @pytest.fixture
    def field(self):
        return Field()

    def test_bound_data_disabled(self, field):
        field.disabled = True
        initial_data = "initial_value"
        data = "submitted_value"
        result = field.bound_data(data, initial_data)
        assert result == initial_data

    def test_bound_data_enabled(self, field):
        field.disabled = False
        initial_data = "initial_value"
        data = "submitted_value"
        result = field.bound_data(data, initial_data)
        assert result == data

    def test_bound_data_with_none_data(self, field):
        field.disabled = False
        initial_data = "initial_value"
        data = None
        result = field.bound_data(data, initial_data)
        assert result is None

    def test_bound_data_with_none_initial(self, field):
        field.disabled = False
        initial_data = None
        data = "submitted_value"
        result = field.bound_data(data, initial_data)
        assert result == data