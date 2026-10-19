import pytest
from django.contrib.admindocs.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases for the function
    test_cases = [
        # No unnamed groups
        (r'^/path/to/resource$', r'^/path/to/resource$'),
        # One unnamed group
        (r'^(?P<name>\w+)/b/(\w+)$', r'^(?P<name>\w+)/b/<var>$'),
        # Nested unnamed groups
        (r'^(?P<name>\w+)/b/((x|y)\w+)$', r'^(?P<name>\w+)/b/<var>$'),
        # Multiple unnamed groups
        (r'^(?P<name>\w+)/b/(\w+)/(foo|bar)$', r'^(?P<name>\w+)/b/<var>/(foo|bar)$'),
        # No groups at all
        (r'^(foo|bar)$', r'^(foo|bar)$'),
        # Handling an empty pattern
        (r'', r''),
        # Multiple unnamed groups with overlapping
        (r'^(?P<name>\w+)/b/((\d+)|(\w+))$', r'^(?P<name>\w+)/b/<var>$'),
    ]

    for pattern, expected in test_cases:
        result = replace_unnamed_groups(pattern)
        assert result == expected, f'Expected {expected}, but got {result} for pattern {pattern}'