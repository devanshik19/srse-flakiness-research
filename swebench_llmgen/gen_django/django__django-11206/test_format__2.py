import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.numberformat import format

@pytest.mark.parametrize("input_number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, expected", [
    (123456.789, ".", None, 0, "", False, mark_safe("123456.789")),
    (123456.789, ".", 2, 0, "", False, mark_safe("123456.79")),
    (123456.789, ".", 4, 0, "", False, mark_safe("123456.7890")),
    (-123456.789, ".", 2, 0, "", False, mark_safe("-123456.79")),
    (Decimal('123456.789'), ".", None, 0, "", False, mark_safe("123456.789")),
    (Decimal('123456.789'), ".", 2, 0, "", False, mark_safe("123456.79")),
    (Decimal('123456.789'), ".", 4, 0, "", False, mark_safe("123456.7890")),
    (Decimal('1234.56789'), ".", 2, (3, 2), ",", True, mark_safe("1,234.57")),
    (Decimal('1234.56789'), ".", None, (3, 2), ",", True, mark_safe("1,234")),
    (Decimal('12345678901234567890123456789012345.67890'), ".", 2, 0, "", False, mark_safe("1.2345678901234567890123456789012345e+34")),
])
def test_format(input_number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping, expected):
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    result = format(input_number, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping)
    assert result == expected