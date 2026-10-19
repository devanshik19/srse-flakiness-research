import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

def test_replace_named_groups():
    # Test case 1: Basic named group
    pattern1 = r"(?P<a>\w+)/b/(\w+)"
    expected1 = r"<a>/b/(\w+)"
    assert replace_named_groups(pattern1) == expected1

    # Test case 2: Multiple named groups
    pattern2 = r"(?P<a>\w+)/b/(?P<c>\w+)"
    expected2 = r"<a>/b/<c>"
    assert replace_named_groups(pattern2) == expected2

    # Test case 3: Nested named groups
    pattern3 = r"(?P<a>(x|y))/b/(?P<c>(z|w))"
    expected3 = r"<a>/b/<c>"
    assert replace_named_groups(pattern3) == expected3

    # Test case 4: Named group with escaped parentheses
    pattern4 = r"(?P<a>\w+)/b/\(test\)"
    expected4 = r"<a>/b/\(test\)"
    assert replace_named_groups(pattern4) == expected4

    # Test case 5: No named groups in pattern
    pattern5 = r"/b/(\w+)"
    expected5 = r"/b/(\w+)"
    assert replace_named_groups(pattern5) == expected5

    # Test case 6: Multiple named groups with mixed characters
    pattern6 = r"(?P<param1>\d+)/(?P<param2>\D+)"
    expected6 = r"<param1>/<param2>"
    assert replace_named_groups(pattern6) == expected6