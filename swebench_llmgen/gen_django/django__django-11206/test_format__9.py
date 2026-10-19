import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.numberformat import format

def test_format_integer_no_grouping():
    assert format(1234, '.', None, 0) == mark_safe(1234)

def test_format_integer_with_grouping():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(1234567, '.', None, 3, ',') == '1,234,567'

def test_format_decimal_no_grouping():
    assert format(Decimal('1234.5678'), '.', 2, 0) == '1234.57'

def test_format_decimal_with_grouping():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(Decimal('1234567.891'), '.', 2, 3, ',') == '1,234,567.89'

def test_format_negative_number():
    assert format(-1234.56, '.', 2) == '-1234.56'

def test_format_large_decimal():
    num = Decimal('1.' + '0' * 210)  # Exceeds 200 digits
    assert format(num, '.', None) == '1e+210'

def test_format_with_forced_grouping():
    assert format(1234567, '.', None, 3, ',', True) == '1,234,567'

def test_format_with_nonuniform_grouping():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(1234567, '.', None, (3, 2), ',') == '1,234,57'

def test_format_with_zero_grouping():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(1234567, '.', None, 0) == '1234567'

def test_format_decimals_with_padding():
    assert format(123.4, '.', 2) == '123.40'