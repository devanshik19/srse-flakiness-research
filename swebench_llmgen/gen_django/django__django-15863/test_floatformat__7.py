import pytest
from decimal import Decimal
from django.template.defaultfilters import floatformat
from django.utils.safestring import mark_safe

def test_floatformat():
    # Test cases for various inputs
    assert floatformat(34.23234) == mark_safe("34.2")
    assert floatformat(34.00000) == mark_safe("34")
    assert floatformat(34.26000) == mark_safe("34.3")
    
    assert floatformat(34.23234, 3) == mark_safe("34.232")
    assert floatformat(34.00000, 3) == mark_safe("34.000")
    assert floatformat(34.26000, 3) == mark_safe("34.260")
    
    assert floatformat(34.23234, -3) == mark_safe("34.232")
    assert floatformat(34.00000, -3) == mark_safe("34")
    assert floatformat(34.26000, -3) == mark_safe("34.260")
    
    assert floatformat(6666.6666, "2g") == mark_safe("6,666.67")
    assert floatformat(10000, 'g') == mark_safe("10,000")
    
    assert floatformat(66666.6666, "2") == mark_safe("66666,67")
    assert floatformat(66666.6666, "2u") == mark_safe("66666.67")

    # Test for edge cases
    assert floatformat(float('inf')) == "inf"
    assert floatformat(float('nan')) == "nan"

    # Test invalid inputs
    assert floatformat("invalid") == ""
    assert floatformat(None) == ""
    assert floatformat("123abc") == ""
    assert floatformat(Decimal('NaN')) == "nan"