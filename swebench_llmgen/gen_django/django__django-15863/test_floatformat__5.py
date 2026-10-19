import pytest
from decimal import Decimal
from django.template.defaultfilters import floatformat


def test_floatformat():
    # Test cases for default behavior with no argument
    assert floatformat(34.23234) == "34.2"
    assert floatformat(34.00000) == "34"
    assert floatformat(34.26000) == "34.3"
    
    # Test cases for positive decimal places
    assert floatformat(34.23234, 3) == "34.232"
    assert floatformat(34.00000, 3) == "34.000"
    assert floatformat(34.26000, 3) == "34.260"

    # Test cases for negative decimal places
    assert floatformat(34.23234, -3) == "34.232"
    assert floatformat(34.00000, -3) == "34"
    assert floatformat(34.26000, -3) == "34.260"

    # Test cases for grouping by thousand
    assert floatformat(6666.6666, "2g") == "6,666.67"
    assert floatformat(10000, "g") == "10,000"

    # Test cases for unlocalized output
    assert floatformat(66666.6666, "2u") == "66666.67"
    
    # Test invalid input cases
    assert floatformat("not a number") == ""
    assert floatformat(None) == ""
    assert floatformat(float('nan')) == "nan"
    assert floatformat(float('inf')) == "inf"
    assert floatformat(float('-inf')) == "-inf"

    # Test float with Large Decimal Places
    assert floatformat(123.456789, 10) == "123.4567890000"