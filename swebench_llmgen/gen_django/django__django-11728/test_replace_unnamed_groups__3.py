import pytest
from django.contrib.admin.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases
    test_cases = [
        ("^(?P<a>\\w+)/b/(\\w+)$", "^(?P<a>\\w+)/b/<var>$"),
        ("^(?P<a>\\w+)/b/((x|y)\\w+)$", "^(?P<a>\\w+)/b/<var>$"),
        ("^(?P<a>\\w+)/b/(\\w+)/(\\w+)$", "^(?P<a>\\w+)/b/<var>/<var>$"),
        ("^/api/(?P<group>[^/]+)/([^/]+)$", "^/api/(?P<group>[^/]+)/<var>$"),
        ("^/path/with/no/groups$", "^/path/with/no/groups$"),
        ("^(\\w+)/(\\w+)$", "<var>/<var>$"),
        ("^(?P<name>\\w+)/archive/(?P<year>\\d{4})$", "^(?P<name>\\w+)/archive/<var>$"),
    ]

    for pattern, expected in test_cases:
        assert replace_unnamed_groups(pattern) == expected