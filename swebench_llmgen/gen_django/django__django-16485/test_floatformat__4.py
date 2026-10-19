import pytest
from decimal import Decimal
from django.utils import formats
from django.template.defaultfilters import floatformat

def test_floatformat():
    # Test cases with different inputs and expected outputs
    test_cases = [
        # Normal cases
        (34.23234, -1, "34.2"),
        (34.00000, -1, "34"),
        (34.26000, -1, "34.3"),
        (34.23234, 3, "34.232"),
        (34.00000, 3, "34.000"),
        (34.26000, 3, "34.260"),
        (6666.6666, "2g", "6,666.67"),
        (10000, "g", "10,000"),
        
        # Negative decimal places
        (34.23234, -3, "34.232"),
        (34.00000, -3, "34"),
        (34.26000, -3, "34.260"),
        
        # Without localization
        (66666.6666, "2u", "66666.67"),
        
        # Edge cases
        (float('inf'), -1, "inf"),
        (float('-inf'), -1, "-inf"),
        (float('nan'), -1, "nan"),
        
        # Invalid input cases
        ("invalid", -1, ""),
        ("not a float", 1, ""),
        (None, -1, ""),
    ]

    for (text, arg, expected) in test_cases:
        assert floatformat(text, arg) == formats.mark_safe(expected)