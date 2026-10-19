import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.numberformat import format

def test_format_integer_without_grouping():
    assert format(123456, '.', None, 0) == mark_safe(123456)

def test_format_integer_with_thousand_separator():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(1234567, '.', None, 3, ',') == mark_safe('1,234,567')

def test_format_float_no_decimal_pos():
    assert format(1234.5678, '.', None) == mark_safe('1234.5678')

def test_format_float_with_decimal_pos():
    assert format(1234.5678, '.', 2) == mark_safe('1234.56')

def test_format_negative_integer():
    assert format(-123456, '.', None, 0) == mark_safe('-123456')

def test_format_negative_float():
    assert format(-1234.5678, '.', 2) == mark_safe('-1234.56')

def test_format_decimal_too_large():
    num = Decimal('1.' + '0' * 205)
    assert format(num, '.', None) == mark_safe('1.0e+205')

def test_format_decimal_with_grouping():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    num = Decimal('1234567.89')
    assert format(num, '.', 2, 3, ',') == mark_safe('1,234,567.89')

def test_format_with_non_integer_grouping():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(123456789, '.', None, (3, 2), ',') == mark_safe('123,456,78,9')

def test_format_with_custom_separator():
    settings.USE_L10N = False
    assert format(1234567, ',', None, 3, '.') == mark_safe('1.234.567')

def test_format_with_force_grouping():
    settings.USE_L10N = False
    assert format(123456789, '.', None, 3, ',', True) == mark_safe('123,456,789')