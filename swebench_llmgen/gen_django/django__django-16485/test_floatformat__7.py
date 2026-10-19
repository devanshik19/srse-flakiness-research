import pytest
from django.utils.formats import number_format
from django.utils.html import mark_safe
from decimal import Decimal, InvalidOperation
from django.template.defaultfilters import floatformat

def test_floatformat():
    # Testing basic float formatting
    assert floatformat(34.23234) == mark_safe("34.2")
    assert floatformat(34.00000) == mark_safe("34")
    assert floatformat(34.26000) == mark_safe("34.3")
    
    # Testing with specified decimal places
    assert floatformat(34.23234, 3) == mark_safe("34.232")
    assert floatformat(34.00000, 3) == mark_safe("34.000")
    assert floatformat(34.26000, 3) == mark_safe("34.260")
    
    # Testing with negative decimal places
    assert floatformat(34.23234, -3) == mark_safe("34.232")
    assert floatformat(34.00000, -3) == mark_safe("34")
    assert floatformat(34.26000, -3) == mark_safe("34.260")
    
    # Testing with grouping
    assert floatformat(6666.6666, '2g') == mark_safe("6,666.67")
    assert floatformat(10000, 'g') == mark_safe("10,000")
    
    # Testing with unlocalized
    assert floatformat(66666.6666, '2u') == mark_safe("66666.67")
    
    # Handling infinity and NaN values
    assert floatformat(float('nan')) == 'nan'
    assert floatformat(float('inf')) == 'inf'
    assert floatformat(float('-inf')) == '-inf'
    
    # Testing invalid input
    assert floatformat("invalid") == ""
    assert floatformat(Decimal('invalid')) == ""
    
    # Testing empty input
    assert floatformat("") == ""
    
    # Testing float rounding with edge cases
    assert floatformat(0.123456, 5) == mark_safe("0.12346")
    assert floatformat(0.123456, 2) == mark_safe("0.12")