import pytest
from decimal import Decimal
from django.template.defaultfilters import floatformat

def test_floatformat():
    assert floatformat(34.23234) == "34.2"
    assert floatformat(34.00000) == "34"
    assert floatformat(34.26000) == "34.3"

    assert floatformat(34.23234, 3) == "34.232"
    assert floatformat(34.00000, 3) == "34.000"
    assert floatformat(34.26000, 3) == "34.260"

    assert floatformat(34.23234, -3) == "34.232"
    assert floatformat(34.00000, -3) == "34"
    assert floatformat(34.26000, -3) == "34.260"

    assert floatformat(6666.6666, "2g") == "6,666.67"
    assert floatformat(10000, "g") == "10,000"

    assert floatformat(66666.6666, "2") == "66666,67"
    assert floatformat(66666.6666, "2u") == "66666.67"

    assert floatformat(float('inf')) == "inf"
    assert floatformat(float('-inf')) == "-inf"
    assert floatformat(float('nan')) == "nan"

    assert floatformat("not a number") == ""
    assert floatformat("1234") == "1,234"
    assert floatformat("1234.5678", 2) == "1,234.57"
    assert floatformat("1234.5678", "3") == "1,234.568"
    assert floatformat("1234.5678", "-1") == "1,234.6"
    assert floatformat("1234.5678", "-2g") == "1,234.57"