import pytest
from django.template.defaultfilters import floatformat
from decimal import Decimal, InvalidOperation

def test_floatformat_no_arg():
    assert floatformat(34.23234) == "34.2"
    assert floatformat(34.00000) == "34"
    assert floatformat(34.26000) == "34.3"

def test_floatformat_positive_arg():
    assert floatformat(34.23234, 3) == "34.232"
    assert floatformat(34.00000, 3) == "34.000"
    assert floatformat(34.26000, 3) == "34.260"

def test_floatformat_negative_arg():
    assert floatformat(34.23234, -3) == "34.232"
    assert floatformat(34.00000, -3) == "34"
    assert floatformat(34.26000, -3) == "34.260"

def test_floatformat_grouping():
    assert floatformat(6666.6666, "2g") == "6,666.67"
    assert floatformat(10000, "g") == "10,000"

def test_floatformat_non_localized():
    assert floatformat(66666.6666, "2u") == "66666.67"

def test_floatformat_invalid_input():
    assert floatformat("invalid") == ""
    assert floatformat(None) == ""
    assert floatformat(float('nan')) == "nan"
    assert floatformat(float('inf')) == "inf"
    assert floatformat(float('-inf')) == "-inf"

def test_floatformat_edge_cases():
    assert floatformat(0.0001, 3) == "0.000"
    assert floatformat(0.9999, 3) == "1.000"
    assert floatformat(-0.9999, 3) == "-1.000"
    assert floatformat(1e-10, 5) == "0.00000"