import pytest
from django.template.defaultfilters import floatformat
from decimal import Decimal

def test_floatformat():
    # Test cases based on the function's documentation

    # Test without argument
    assert floatformat(34.23234) == "34.2"
    assert floatformat(34.00000) == "34"
    assert floatformat(34.26000) == "34.3"
    
    # Test with positive argument
    assert floatformat(34.23234, 3) == "34.232"
    assert floatformat(34.00000, 3) == "34.000"
    assert floatformat(34.26000, 3) == "34.260"

    # Test with negative argument
    assert floatformat(34.23234, -3) == "34.232"
    assert floatformat(34.00000, -3) == "34"
    assert floatformat(34.26000, -3) == "34.260"

    # Test with grouping ('g' suffix)
    assert floatformat(6666.6666, "2g") == "6,666.67"
    assert floatformat(10000, "g") == "10,000"

    # Test with unlocalized ('u' suffix)
    assert floatformat(66666.6666, "2u") == "66666.67"
  
    # Test with infinity and NaN
    assert floatformat(float('inf')) == "inf"
    assert floatformat(float('-inf')) == "-inf"
    assert floatformat(float('nan')) == "nan"

    # Test with invalid input (string and float)
    assert floatformat("not a number") == ""
    assert floatformat(None) == ""
    
    # Test precision errors
    assert floatformat('10.12345', 'x') == '10.12345'  # invalid arg should return input
    assert floatformat('10.12345', '1g') == '10.1'  # forcing grouping with decimal places