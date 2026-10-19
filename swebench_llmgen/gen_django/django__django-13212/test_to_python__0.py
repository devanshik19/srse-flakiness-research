import pytest
from django.forms.fields import Field

@pytest.mark.parametrize("input_value, expected_output", [
    (None, None),
    ("test", "test"),
    (123, 123),
    (3.14, 3.14),
    (True, True),
])
def test_to_python(input_value, expected_output):
    field = Field()
    assert field.to_python(input_value) == expected_output