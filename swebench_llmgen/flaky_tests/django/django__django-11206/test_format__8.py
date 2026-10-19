import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.numberformat import format

def test_format_integer_no_grouping():
    assert format(123456, '.', None, 0) == mark_safe(123456)

def test_format_integer_with_grouping():
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(1234567, '.', None, 3, ',') == '1,234,567'

def test_format_decimal_no_decimal_pos():
    assert format(Decimal('1234.5678'), '.', None) == '1234.5678'

def test_format_decimal_with_decimal_pos():
    assert format(Decimal('1234.5678'), '.', 2) == '1234.56'

def test_format_decimal_exceeding_length():
    assert format(Decimal('1e300'), '.', None) == '1e300'

def test_format_negative_integer():
    assert format(-1234567, '.', None, 3, ',') == '-1,234,567'

def test_format_negative_decimal_with_decimal_pos():
    assert format(Decimal('-1234.5678'), '.', 3) == '-1234.567'

def test_format_float_no_grouping():
    assert format(123456.789, '.', None, 0) == '123456.789'

def test_format_float_with_grouping():
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(1234567.89, '.', None, 3, ',') == '1,234,567.89'

def test_format_decimal_with_forced_grouping():
    settings.USE_THOUSAND_SEPARATOR = False
    assert format(1234567.89, '.', None, 3, ',') == '1,234,567.89'

def test_format_float_with_custom_thousand_sep():
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(1234567.89, '.', None, 3, ' ') == '1 234 567.89'