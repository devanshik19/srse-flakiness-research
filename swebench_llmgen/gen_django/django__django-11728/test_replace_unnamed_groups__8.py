import pytest
from django.contrib.admindocs.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases with expected output
    test_cases = [
        (r'^(?P<a>\w+)/b/(\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<a>\w+)/b/((x|y)\w+)$', r'^(?P<a>\w+)/b/<var>$'),
        (r'^(?P<a>\w+)/(b/(\w+))?$', r'^(?P<a>\w+)/(b/<var>)?$'),
        (r'^(?P<a>\w+)/((b|\w+))$', r'^(?P<a>\w+)/<var>$'),
        (r'^(?P<a>\w+)$', r'^(?P<a>\w+)$'),
        (r'^(?P<a>\w+)/b/((x|y)\w+)/(c/d)$', r'^(?P<a>\w+)/b/<var>/(c/d)$'),
    ]

    for pattern, expected in test_cases:
        result = replace_unnamed_groups(pattern)
        assert result == expected, f'For pattern: {pattern}, expected: {expected}, got: {result}'

    # Edge case with no unnamed groups
    assert replace_unnamed_groups('^test_pattern$') == '^test_pattern$'

    # Edge case with only unnamed groups
    assert replace_unnamed_groups('(^test_pattern|(?P<name>other_pattern))') == '(^test_pattern|(?P<name>other_pattern))'