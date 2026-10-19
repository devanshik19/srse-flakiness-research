import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

def test_replace_named_groups():
    # Test cases for replacement of named groups in the pattern

    # Case 1: Single named group
    pattern_1 = r'^(?P<a>\w+)/b/(\w+)$'
    expected_1 = r'^<a>/b/(\w+)$'
    assert replace_named_groups(pattern_1) == expected_1

    # Case 2: Multiple named groups
    pattern_2 = r'^(?P<a>\w+)/b/(?P<c>\w+)/$'
    expected_2 = r'^<a>/b/<c>/$'
    assert replace_named_groups(pattern_2) == expected_2

    # Case 3: Nested named group
    pattern_3 = r'^(?P<a>(?P<b>\w+))/b/(?P<c>\w+)/$'
    expected_3 = r'^<a>/b/<c>/$'
    assert replace_named_groups(pattern_3) == expected_3

    # Case 4: Named group at the end
    pattern_4 = r'^(?P<user_id>\d+)/profile/(?P<username>\w+)$'
    expected_4 = r'^<user_id>/profile/<username>$'
    assert replace_named_groups(pattern_4) == expected_4

    # Case 5: Pattern without named groups
    pattern_5 = r'^\w+/b/\w+$'
    expected_5 = pattern_5  # No change expected
    assert replace_named_groups(pattern_5) == expected_5

    # Case 6: Escaped parentheses
    pattern_6 = r'^(?P<a>\(x\|y\))/b/(?P<c>\w+)/$'
    expected_6 = r'^<a>/b/<c>/$'
    assert replace_named_groups(pattern_6) == expected_6