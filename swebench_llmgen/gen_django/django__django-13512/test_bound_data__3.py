import pytest
from django.forms import Field

@pytest.mark.django_db
def test_bound_data_with_disabled_field():
    field = Field()
    field.disabled = True
    initial_data = "initial_value"
    submitted_data = "submitted_value"

    result = field.bound_data(submitted_data, initial_data)
    assert result == initial_data  # Should return initial data when disabled

@pytest.mark.django_db
def test_bound_data_with_enabled_field():
    field = Field()
    field.disabled = False
    initial_data = "initial_value"
    submitted_data = "submitted_value"

    result = field.bound_data(submitted_data, initial_data)
    assert result == submitted_data  # Should return submitted data when enabled