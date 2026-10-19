import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.numberformat import format

@pytest.mark.parametrize("number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n, expected", [
    (1234567, ',', None, 0, '', False, None, mark_safe("1234567")),
    (1234567.89, '.', 2, 0, '', False, None, mark_safe("1234567.89")),
    (Decimal('12345678.901234'), '.', 4, 0, '', False, None, mark_safe("12345678.9012")),
    (Decimal('1000000.12345'), '.', 3, (3, 2), ',', True, None, mark_safe("1,000,000.123")),
    (-Decimal('9876543.21'), '.', 2, 3, ',', False, None, mark_safe("-9,876,543.21")),
    (Decimal('1e200'), '.', None, 0, '', False, None, mark_safe("1.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e200")),
])
def test_format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n, expected):
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    result = format(number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, use_l10n)
    assert result == expected