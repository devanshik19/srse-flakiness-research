import pytest
from django.template.defaultfilters import floatformat
from decimal import Decimal, InvalidOperation

def test_floatformat():
    # Test with positive decimal
    assert floatformat(34.23234) == "34.2"
    assert floatformat(34.00000) == "34"
    assert floatformat(34.26000) == "34.3"
    
    # Test with specific decimal places
    assert floatformat(34.23234, 3) == "34.232"
    assert floatformat(34.00000, 3) == "34.000"
    assert floatformat(34.26000, 3) == "34.260"
    
    # Test with negative decimal places
    assert floatformat(34.23234, -3) == "34.232"
    assert floatformat(34.00000, -3) == "34"
    assert floatformat(34.26000, -3) == "34.260"
    
    # Test with grouping
    assert floatformat(6666.6666, "2g") == "6,666.67"
    assert floatformat(10000, "g") == "10,000"
    
    # Test with unlocalizing
    assert floatformat(66666.6666, "2u") == "66666.67"
    
    # Test with special cases: infinity and NaN
    assert floatformat(float('inf')) == "inf"
    assert floatformat(float('nan')) == "nan"
    
    # Test with invalid input
    assert floatformat("not a number") == ""
    assert floatformat(None) == ""
    
    # Test with extremely large or small decimals
    assert floatformat(Decimal('1.234567890123456789'), 10) == "1.2345678901"
    assert floatformat(Decimal('0.00000000012345'), 10) == "0.0000000001"