import pytest
from django.contrib.admindocs.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases to cover different scenarios
    test_cases = [
        # No unnamed groups
        ("^users/(?P<id>\\d+)$", "^users/(?P<id>\\d+)$"),
        # One unnamed group
        ("^b/(\\w+)$", "^b/<var>$"),
        # Nested unnamed group
        ("^b/((x|y)\\w+)$", "^b/<var>$"),
        # Multiple unnamed groups
        ("^(\\w+)/b/(\\w+)$", "^<var>/b/<var>$"),
        # Unnamed group followed by named group
        ("^(?P<name>\\w+)/b/(\\d+)$", "^(?P<name>\\w+)/b/<var>$"),
        # Edge case with escaped parentheses
        ("^users/(\\(id\\))?$", "^users/<var>$"),
        # Complex pattern
        ("^(?P<arg1>\\w+)/(\\(arg2\\))?/(\\w+)$", "^(?P<arg1>\\w+)/<var>/\\w+$"),
        # No groups
        ("^no_groups_here$", "^no_groups_here$"),
        # Single character
        ("^(x)$", "^(x)$"),
        # No unmatched group should be replaced
        ("^a/(b|c)$", "^a/<var>$"),
    ]

    for pattern, expected in test_cases:
        result = replace_unnamed_groups(pattern)
        assert result == expected