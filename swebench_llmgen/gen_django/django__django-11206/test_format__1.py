import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.numberformat import format

@pytest.mark.parametrize("number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n, expected", [
    (1234567, ',', None, 0, '', False, None, mark_safe("1234567")),
    (Decimal('1234567.89'), '.', 2, 0, '', False, None, "1234567.89"),
    (Decimal('1234567.89'), '.', 2, 0, ',', False, None, "1234567.89"),
    (Decimal('1234567.89'), '.', None, 3, ',', False, None, "1,234,567"),
    (Decimal('1234567.89'), ',', 2, 3, ',', False, None, "1.234.567,89"),
    (Decimal('12000.00'), ',', 2, (3, 2), ',', False, None, "12.000,00"),
    (Decimal('1234567890123456789012345678901234567890'), '.', None, 0, '', False, None, "1.2345678901234567e+39"),
    (-12345.6789, '.', 2, 0, '', False, None, "-12345.68"),
    (0, '.', None, 0, '', False, None, mark_safe("0")),
    (None, '.', None, 0, '', False, None, "None"),
])

def test_format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n, expected):
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    result = format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n)
    assert result == expected