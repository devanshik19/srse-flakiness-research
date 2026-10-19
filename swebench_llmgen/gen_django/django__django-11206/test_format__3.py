import pytest
from decimal import Decimal
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils.numberformat import format


def test_format_integer_no_grouping():
    assert format(1234567890, '.', None, 0, '') == mark_safe(1234567890)


def test_format_integer_with_grouping():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert format(1234567890, '.', None, 3, ',') == '1,234,567,890'


def test_format_decimal_no_decimal_pos():
    assert format(Decimal('1234567.89'), '.', None, 0, '') == '1234567.89'


def test_format_decimal_with_decimal_pos():
    assert format(Decimal('1234567.89'), '.', 1, 0, '') == '1234567.8'


def test_format_decimal_over_200_digits():
    long_decimal = Decimal('1.' + '0' * 202)
    assert format(long_decimal, '.', None, 0, '') == '1e+202'


def test_format_negative_integer():
    assert format(-1234567890, '.', None, 0, '') == '-1234567890'


def test_format_negative_decimal():
    assert format(Decimal('-1234567.89'), '.', None, 0, '') == '-1234567.89'


def test_format_with_custom_thousand_sep():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True
    assert (
        format(1234567890, '.', None, 3, ' ') == '1 234 567 890'
    )


def test_format_with_force_grouping():
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = False
    assert format(1234567890, '.', None, 2, ',', force_grouping=True) == '1,23,45,67,89,0'