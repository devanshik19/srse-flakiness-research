import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.numberformat import format

@pytest.mark.parametrize("number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n, expected", [
    (1234567.89, '.', 2, 0, '', False, None, '1234567.89'),
    (1234567.89, ',', 2, 0, '', False, None, '1234567.89'),
    (1234567.89, '.', 2, 3, ',', False, None, '1,234,567.89'),
    (1234567.89, '.', None, 3, ',', False, None, '1,234,567'),
    (Decimal('1234567.89'), '.', 2, 0, '', False, None, mark_safe('1234567.89')),
    (Decimal('1234567.89'), '.', 2, 3, ',', False, None, mark_safe('1,234,567.89')),
    (Decimal('123456789012345678901234567890'), '.', None, 3, ',', False, None, '1,234,567,890,123,456,789,012,345,678,901,234,567,890'),
    (-1234.56, '.', 2, 3, ',', False, None, '-1,234.56'),
    (1234.0, '.', None, 0, '', True, None, '1234'),
    (0, '.', None, 0, '', False, None, '0'),
])

def test_format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n, expected):
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    result = format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n)
    assert result == expected

def test_format_integer_without_grouping():
    assert format(1000, '.', None, 0, '', False, None) == mark_safe(1000)

def test_format_decimal_without_grouping():
    assert format(Decimal('1000.1234'), '.', 2, 0, '', False, None) == mark_safe('1000.12')

def test_format_zero():
    assert format(0, '.', None, 0, '', False, None) == '0'