import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

def test_replace_named_groups():
    # Test cases
    test_cases = [
        # Simple named group
        (r'^(?P<a>\w+)/b/(\w+)$', r'^[a]/b/(\w+)$'),
        # Multiple named groups
        (r'^(?P<a>\w+)/b/(?P<c>\w+)/$', r'^[a]/b/[c]/$'),
        # Nested named group
        (r'^(?P<a>(x|y))/b/(?P<c>\w+)/$', r'^[a]/b/[c]/$'),
        # Edge case with no named groups
        (r'^\w+/b/\w+$', r'^\w+/b/\w+$'),
        # Named group with escaped parentheses
        (r'^(?P<a>\(x\))/b/(?P<c>\w+)/$', r'^[a]/b/[c]/$'),
        # Multiple different patterns
        (r'^(?P<a>\w+)/b/(?P<c>\w+)(?P<d>\d+)$', r'^[a]/b/[c][d]$')
    ]

    for pattern, expected in test_cases:
        result = replace_named_groups(pattern)
        assert result == expected, f"Expected '{expected}', got '{result}' for pattern '{pattern}'"

    # Check with invalid patterns, expecting no replacement
    invalid_pattern = r'^(?P<a>\w+)(\w+)$'  
    result_invalid = replace_named_groups(invalid_pattern)
    assert result_invalid == invalid_pattern, f"Expected '{invalid_pattern}', got '{result_invalid}' for pattern '{invalid_pattern}'"