import pytest
from django.template.defaultfilters import floatformat

def test_floatformat():
    # Test with different float values
    assert floatformat(34.23234) == "34.2"
    assert floatformat(34.00000) == "34"
    assert floatformat(34.26000) == "34.3"
    assert floatformat(6666.6666, 2) == "6666.67"
    assert floatformat(10000, 'g') == "10,000"
    assert floatformat(66666.6666, '2u') == "66666.67"
    
    # Test with negative decimal places
    assert floatformat(34.23234, -3) == "34.232"
    assert floatformat(34.00000, -3) == "34"
    assert floatformat(34.26000, -3) == "34.260"
    
    # Test with invalid input
    assert floatformat("invalid") == ""
    assert floatformat(None) == ""
    
    # Test with special values: NaN and Infinity
    assert floatformat(float('nan')) == "nan"
    assert floatformat(float('inf')) == "Infinity"
    assert floatformat(float('-inf')) == "-Infinity"
    
    # Test with strings and variations in precision and grouping
    assert floatformat("34.56789", 4) == "34.5679"
    assert floatformat("34.56789", "3g") == "34.568"
    assert floatformat("10000.12345", "g") == "10,000.12"

    # Test case with rounding
    assert floatformat(34.555, 2) == "34.56"
    assert floatformat(34.554, 2) == "34.55"