import pytest
from django.forms import Field

@pytest.mark.parametrize("data, initial, disabled, expected", [
    (None, 'initial_value', False, None),
    ('submitted_value', 'initial_value', False, 'submitted_value'),
    ('submitted_value', 'initial_value', True, 'initial_value'),
    (42, 'initial_value', False, 42),
    (3.14, None, False, 3.14),
    ('', 'initial_value', False, ''),
])
def test_bound_data(data, initial, disabled, expected):
    field = Field()
    field.disabled = disabled
    result = field.bound_data(data, initial)
    assert result == expected