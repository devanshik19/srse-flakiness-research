import pytest
from django.utils.formats import number_format
from decimal import Decimal
from django.utils.html import mark_safe
from django.template.defaultfilters import floatformat

@pytest.mark.parametrize("input_val, arg, expected_output", [
    (34.23234, None, mark_safe("34.2")),
    (34.00000, None, mark_safe("34")),
    (34.26000, None, mark_safe("34.3")),
    (34.23234, 3, mark_safe("34.232")),
    (34.00000, 3, mark_safe("34.000")),
    (34.26000, 3, mark_safe("34.260")),
    (34.23234, -3, mark_safe("34.232")),
    (34.00000, -3, mark_safe("34")),
    (34.26000, -3, mark_safe("34.260")),
    (6666.6666, '2g', mark_safe("6,666.67")),
    (10000, 'g', mark_safe("10,000")),
    (66666.6666, '2', mark_safe("66666.67")),
    (66666.6666, '2u', mark_safe("66666.67")),
    (float('inf'), None, mark_safe("inf")),
    (float('-inf'), None, mark_safe("-inf")),
    (float('nan'), None, mark_safe("nan")),
    ("invalid", None, ""),
    ("123.456", "invalid_arg", "123.456"),
])
def test_floatformat(input_val, arg, expected_output):
    assert floatformat(input_val, arg) == expected_output