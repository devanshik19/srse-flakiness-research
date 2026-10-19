import pytest
from django.forms.fields import Field

@pytest.mark.parametrize("data, initial, disabled, expected", [
    (None, 'initial_value', False, None),  # Test with data as None
    ('submitted_value', 'initial_value', False, 'submitted_value'),  # Typical case
    (None, None, False, None),  # When both data and initial are None
    (None, 'initial_value', True, 'initial_value'),  # Disabled field should return initial
    ('submitted_value', 'initial_value', True, 'initial_value'),  # Disabled field with submitted value
])
def test_bound_data(data, initial, disabled, expected):
    field = Field()
    field.disabled = disabled
    result = field.bound_data(data, initial)
    assert result == expected