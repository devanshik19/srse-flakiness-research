import pytest
from django.template.defaultfilters import floatformat
from decimal import Decimal

def test_floatformat():
    # Testing various float inputs with different format specifiers
    assert floatformat(34.23234) == "34.2"
    assert floatformat(34.00000) == "34"
    assert floatformat(34.26000) == "34.3"
    assert floatformat(34.23234, 3) == "34.232"
    assert floatformat(34.00000, 3) == "34.000"
    assert floatformat(34.26000, 3) == "34.260"
    assert floatformat(34.23234, -3) == "34.232"
    assert floatformat(34.00000, -3) == "34"
    assert floatformat(34.26000, -3) == "34.260"
    
    # Testing the grouping functionality
    assert floatformat(6666.6666, "2g") == "6,666.67"
    assert floatformat(10000, "g") == "10,000"
    assert floatformat(66666.6666, "2u") == "66666.67"
    
    # Testing edge cases
    assert floatformat("abc") == ""
    assert floatformat("NaN") == "NaN"
    assert floatformat("Infinity") == "Infinity"
    
    # Testing handling of invalid operation and strange numbers
    assert floatformat(None) == ""
    assert floatformat(float('inf')) == "Infinity"
    assert floatformat(float('nan')) == "NaN"
    
    # Testing different data types
    assert floatformat(Decimal('34.1111')) == "34.1"
    assert floatformat(Decimal('34.1111'), 2) == "34.11"
    assert floatformat(Decimal('34.0000')) == "34"