import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

def test_replace_named_groups():
    # Test cases for the replace_named_groups function
    test_cases = [
        # Test case with a single named group
        ("^(?P<a>\\w+)/b/(\\w+)$", "^<a>/b/(\\w+)$"),
        # Test case with multiple named groups
        ("^(?P<a>\\w+)/b/(?P<c>\\w+)/?$", "^<a>/b/<c>/$"),
        # Test case with nested named groups
        ("^(?P<a>(x|y))/b/(?P<c>(z|w))/?$", "^<a>/b/<c>/$"),
        # Test case with no named groups
        ("^/b/(\\w+)$", "^/b/(\\w+)$"),
        # Test case with only named groups in different parts of the regex
        ("^(?P<a>\\w+)/(?P<b>\\d+)/$", "^<a>/<b>/$"),
    ]

    for pattern, expected in test_cases:
        result = replace_named_groups(pattern)
        assert result == expected, f"For '{pattern}', expected '{expected}', but got '{result}'"

    # Edge case for empty pattern
    assert replace_named_groups("") == ""