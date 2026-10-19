import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.numberformat import format

def test_format_integer_no_grouping():
    result = format(1234567890, decimal_sep='.', decimal_pos=None, grouping=0)
    assert result == mark_safe(1234567890)

def test_format_decimal_no_grouping():
    result = format(Decimal('1234.5678'), decimal_sep='.', decimal_pos=None, grouping=0)
    assert result == mark_safe('1234.5678')

def test_format_integer_with_grouping():
    result = format(1234567890, decimal_sep='.', decimal_pos=None, grouping=3, thousand_sep=',')
    assert result == mark_safe('1,234,567,890')

def test_format_decimal_with_grouping():
    result = format(Decimal('1234567.89'), decimal_sep='.', decimal_pos=2, grouping=3, thousand_sep=',')
    assert result == mark_safe('1,234,567.89')

def test_format_negative_integer_with_grouping():
    result = format(-1234567890, decimal_sep='.', decimal_pos=None, grouping=3, thousand_sep=',')
    assert result == mark_safe('-1,234,567,890')

def test_format_negative_decimal_with_grouping():
    result = format(Decimal('-1234567.89'), decimal_sep='.', decimal_pos=2, grouping=3, thousand_sep=',')
    assert result == mark_safe('-1,234,567.89')

def test_format_scientific_notation():
    result = format(Decimal('1E200'), decimal_sep='.', decimal_pos=None, grouping=3, thousand_sep=',')
    assert result == mark_safe('1.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e200')

def test_format_decimal_with_position():
    result = format(Decimal('1234.5'), decimal_sep='.', decimal_pos=3, grouping=3, thousand_sep=',')
    assert result == mark_safe('1,234.500')

def test_format_with_force_grouping():
    settings.USE_THOUSAND_SEPARATOR = True
    result = format(1234567, decimal_sep='.', decimal_pos=None, grouping=3, thousand_sep=',', force_grouping=True)
    assert result == mark_safe('1,234,567')

def test_format_no_decimal_sep():
    result = format(12345, decimal_sep='', decimal_pos=None, grouping=3, thousand_sep=',')
    assert result == mark_safe('12,345')

def test_format_decimal_with_long_digit_grouping():
    result = format(Decimal('1234567890.12345'), decimal_sep='.', decimal_pos=3, grouping=(3, 2), thousand_sep=',')
    assert result == mark_safe('1,234,567,890.123')