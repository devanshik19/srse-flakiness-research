import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

def test_replace_named_groups():
    # Test cases to validate the functionality of replace_named_groups
    
    # Test case 1: Single named group
    pattern1 = r'^(?P<a>\w+)/b/(\w+)$'
    expected1 = r'^[a]/b/(\w+)$'
    assert replace_named_groups(pattern1) == expected1

    # Test case 2: Multiple named groups
    pattern2 = r'^(?P<a>\w+)/b/(?P<c>\w+)/$'
    expected2 = r'^[a]/b/[c]/$'
    assert replace_named_groups(pattern2) == expected2

    # Test case 3: Nested named group
    pattern3 = r'^(?P<a>(?P<b>foo|bar))/b/(?P<c>\w+)/$'
    expected3 = r'^[a]/b/[c]/$'  # Outer named group replaced
    assert replace_named_groups(pattern3) == expected3

    # Test case 4: No named groups
    pattern4 = r'^\w+/b/\w+$'
    expected4 = r'^\w+/b/\w+$'  # No change
    assert replace_named_groups(pattern4) == expected4

    # Test case 5: Multiple identical named groups
    pattern5 = r'^(?P<name>\w+)/b/(?P<name>\w+)/$'
    expected5 = r'^[name]/b/[name]/$'  # Both should become [name]
    assert replace_named_groups(pattern5) == expected5

    # Test case 6: Empty string
    pattern6 = r''
    expected6 = r''  # Nothing to replace
    assert replace_named_groups(pattern6) == expected6

    # Test case 7: Special characters with named groups
    pattern7 = r'^(?P<a>[a-zA-Z0-9]+).(?P<b>\d+)$'
    expected7 = r'^[a]. [b]$'  # Named groups replaced with their names
    assert replace_named_groups(pattern7) == expected7

    # Test case 8: Escaped parentheses
    pattern8 = r'^\(P<a>\w+/\(b\)\w+$'
    expected8 = r'^\(P<a>/\(b\)\w+$'  # No replacement due to escape
    assert replace_named_groups(pattern8) == expected8