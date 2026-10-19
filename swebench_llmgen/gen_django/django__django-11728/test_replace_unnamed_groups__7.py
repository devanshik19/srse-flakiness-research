import pytest
from django.contrib.admindocs.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases for unnamed group replacements
    test_cases = [
        # Test case format: (input_pattern, expected_output)
        (r'^(?P<a>\w+)/b/(\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<a>\w+)/b/((x|y)\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<a>\w+)/b/(\w+)/(?:another_group)$', r'^(?P<a>\w+)/b/<var>/(?:another_group)$'),
        (r'^(?P<a>\w+)/b/((x|y)\w+)/(?:also_group)$', r'^(?P<a>\w+)/b/<var>/(?:also_group)$'),
        (r'^(?P<a>\w+)/b/(\w+(?P<extra>\d+))$', r'^(?P<a>\w+)/b/<var>$',),
        (r'^\w+$', r'^\w+$'),  # No unnamed groups
        (r'^(a)(b)$', r'^(a)(b)$'),  # No unnamed groups, no replacement
    ]

    for pattern, expected in test_cases:
        assert replace_unnamed_groups(pattern) == expected