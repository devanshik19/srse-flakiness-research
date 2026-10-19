import pytest
from django.forms.fields import Field

@pytest.mark.parametrize("input_value, expected_output", [
    (None, None),
    ('', ''),
    ('test', 'test'),
    (123, 123),
    (Decimal('10.5'), Decimal('10.5')),
    (datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 1)),
])
def test_to_python(input_value, expected_output):
    field = Field()
    result = field.to_python(input_value)
    assert result == expected_output