import pytest
from django.contrib.admin.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases for unnamed groups
    test_cases = [
        (r'^(?P<a>\w+)/b/(\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<a>\w+)/b/((x|y)\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<name>\w+)/c/(d+|e+)$', r'^(?P<name>\w+)/c/<var>$'),
        (r'^(?P<name>\w+)/c/(|)$', r'^(?P<name>\w+)/c/<var>$'),
        (r'^\w+/(foo|bar)$', r'^\w+/<var>$'),
        (r'^(?P<name>\w+\|)\w+/(foo|bar)$', r'^(?P<name>\w+\|)<var>$'),
        (r'^(?P<name>\w+)/\((foo|bar)\)$', r'^(?P<name>\w+)/<var>$'),
        (r'^\((foo|bar)\)$', r'<var>$'),
        (r'^\w+$', r'^\w+$'),  # No unnamed group
    ]

    for pattern, expected in test_cases:
        assert replace_unnamed_groups(pattern) == expected