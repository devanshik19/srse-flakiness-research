import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.numberformat import format

@pytest.mark.parametrize("number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n, expected", [
    (1234567.89, '.', None, 0, ',', False, None, '1,234,567.89'),
    (1234567.89, ',', 2, 0, '.', False, None, '1.234.567,89'),
    (Decimal('1234567.89'), '.', None, 0, ',', False, None, '1,234,567.89'),
    (Decimal('1234.5678'), '.', 2, 0, ',', False, None, '1,234.57'),
    (Decimal('1234.5678'), '.', 4, 0, ',', False, None, '1,234.5678'),
    (-123456.78, '.', None, 0, ',', False, None, '-123,456.78'),
    (12345.6789, '.', 3, 0, ',', False, None, '12,345.679'),
    (12345.6789, '.', 0, 3, ',', False, None, '12,345'),
    (1234567890123.456, '.', None, 0, ',', False, None, '1,234,567,890,123.456'),
    (123456789.123456789, '.', None, [3, 2], ',', False, None, '123,456,789.123456'),
    (123456789, '.', None, 0, ',', False, None, '1,234,567,89'),
])
def test_format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n, expected):
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n) == mark_safe(expected)

def test_format_without_thousand_sep():
    number = 1234567.89
    decimal_sep = '.'
    decimal_pos = None
    grouping = 0
    thousand_sep = ''
    force_grouping = False
    use_l10n = None
    expected = '1234567.89'
    
    assert format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n) == mark_safe(expected)

def test_format_with_force_grouping():
    number = 1234567.89
    decimal_sep = '.'
    decimal_pos = None
    grouping = 3
    thousand_sep = ','
    force_grouping = True
    use_l10n = None
    expected = '1,234,567.89'
    
    assert format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n) == mark_safe(expected)