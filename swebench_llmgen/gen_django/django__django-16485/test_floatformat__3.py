import pytest
from decimal import Decimal
from django.utils import formats
from django.template.defaultfilters import floatformat

@pytest.mark.parametrize("text, arg, expected", [
    (34.23234, None, "34.2"),
    (34.00000, None, "34"),
    (34.26000, None, "34.3"),
    (34.23234, 3, "34.232"),
    (34.00000, 3, "34.000"),
    (34.26000, 3, "34.260"),
    (34.23234, -3, "34.232"),
    (34.00000, -3, "34"),
    (34.26000, -3, "34.260"),
    (6666.6666, '2g', "6,666.67"),
    (10000, 'g', "10,000"),
    (66666.6666, '2', "66666,67"),
    (66666.6666, '2u', "66666.67"),
    (float('inf'), None, "inf"),
    (float('-inf'), None, "-inf"),
    (float('nan'), None, "nan"),
    ("not a number", None, ""),
    (None, None, ""),
    (Decimal('34.999'), 2, "34.99"),
    (Decimal('34.999'), 'g', "34.99"),
])
def test_floatformat(text, arg, expected):
    result = floatformat(text, arg)
    assert result == expected