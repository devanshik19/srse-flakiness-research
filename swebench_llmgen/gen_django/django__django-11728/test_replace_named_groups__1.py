import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

def test_replace_named_groups():
    # Test cases with expected output
    test_cases = [
        (r'^(?P<a>\w+)/b/(\w+)$', r'^[a]/b/(\w+)$'),
        (r'^(?P<a>\w+)/b/(?P<c>\w+)/$', r'^[a]/b/[c]/$'),
        (r'^(?P<first>\d+)/(?P<second>\w+)$', r'^[first]/[second]$'),
        (r'^(?P<user_id>\d+)/profile/(?P<action>\w+)$', r'^[user_id]/profile/[action]$'),
        (r'^(?P<id>\d+)(/\w+)?$', r'^[id](/\w+)?$'),
        (r'^(?P<group>(?P<nested>\w+))$', r'^[group]$'),
        (r'^(?P<outer>(?P<inner>\d+))$', r'^[outer]$'),
        (r'^\(?(?P<name>\w+)\)?$', r'^[name]$'),
    ]

    for pattern, expected in test_cases:
        result = replace_named_groups(pattern)
        assert result == expected

    # Test with unmatched parenthesis (should not match)
    unmatched_pattern = r'^(?P<invalid>\d+)$('
    result = replace_named_groups(unmatched_pattern)
    assert result == unmatched_pattern  # No changes expected

    # Test with no named groups
    simple_pattern = r'^\d+/b/\w+$'
    result = replace_named_groups(simple_pattern)
    assert result == simple_pattern  # No changes expected