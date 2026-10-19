import pytest
from decimal import Decimal
from django.utils import formats
from django.template.defaultfilters import floatformat

def test_floatformat():
    # Test default behavior with one decimal place
    assert floatformat(34.23234) == formats.number_format("34.2", 1)
    assert floatformat(34.00000) == formats.number_format("34", 0)
    assert floatformat(34.26000) == formats.number_format("34.3", 1)

    # Test positive arg for exact decimal places
    assert floatformat(34.23234, 3) == formats.number_format("34.232", 3)
    assert floatformat(34.00000, 3) == formats.number_format("34.000", 3)
    assert floatformat(34.26000, 3) == formats.number_format("34.260", 3)

    # Test negative arg
    assert floatformat(34.23234, -3) == formats.number_format("34.232", 3)
    assert floatformat(34.00000, -3) == formats.number_format("34", 0)
    assert floatformat(34.26000, -3) == formats.number_format("34.260", 3)

    # Test grouping (with 'g' suffix)
    assert floatformat(6666.6666, "2g") == formats.number_format("6,666.67", 2)
    assert floatformat(10000, "g") == formats.number_format("10,000", 0)

    # Test ungrouping (with 'u' suffix)
    assert floatformat(66666.6666, "2u") == formats.number_format("66666.67", 2)
    assert floatformat(66666.6666, "2") == formats.number_format("66666,67", 2)

    # Test edge cases
    assert floatformat(float('inf')) == 'inf'
    assert floatformat(float('-inf')) == '-inf'
    assert floatformat(float('nan')) == 'nan'
    
    # Test invalid inputs
    assert floatformat("abc") == ""
    assert floatformat("") == ""
    assert floatformat(None) == ""
    assert floatformat("123.45abc") == ""