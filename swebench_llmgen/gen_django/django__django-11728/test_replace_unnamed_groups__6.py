import pytest
from django.contrib.admindocs.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases with expected results
    test_cases = [
        (r'^(?P<a>\w+)/b/(\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<a>\w+)/b/((x|y)\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<a>\w+)/c/(\d+)$', r'^(?P<a>\w+)/c/<var>$'),
        (r'^(?P<a>\w+)/d/((?P<b>\w+)|(\w+))$', r'^(?P<a>\w+)/d/<var>$'),
        (r'^[a-z]+$', r'^[a-z]+$'),
        (r'$', r'$'),
        (r'^(?P<name>\w+)/\d+/(\\(a\\))$', r'^(?P<name>\w+)/\d+/(\\(a\\))$'),
    ]

    for pattern, expected in test_cases:
        assert replace_unnamed_groups(pattern) == expected