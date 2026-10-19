import pytest
from django.contrib.admindocs.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases: (input pattern, expected output)
    test_cases = [
        (r'^(?P<a>\w+)/b/(\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<a>\w+)/b/((x|y)\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<name>\w+)/c/(?P<id>\d+)$', r'^(?P<name>\w+)/c/<var>$'),
        (r'(\w+)-(\w+)', r'<var>-<var>'),  # Multiple unnamed groups
        (r'^(?P<match>\w+)/(?P<rest>.*)$', r'^(?P<match>\w+)/<var>$'),  # Named and unnamed
        (r'^(?P<a>\w+)(\d+)(\w+)$', r'^(?P<a>\w+)<var><var>$'),  # Various groups
        (r'^(a|b)(c|d)$', r'<var><var>$'),  # Groups that are completely unnamed
        (r'^(?P<a>\w+)$', r'^(?P<a>\w+)$'),  # No unnamed groups
        (r'^(.*)$', r'<var>$'),  # Entirely unnamed
    ]

    for pattern, expected in test_cases:
        result = replace_unnamed_groups(pattern)
        assert result == expected, f'For pattern "{pattern}", expected "{expected}" but got "{result}"'