import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

@pytest.mark.parametrize("pattern, expected", [
    (r"^(?P<a>\w+)/b/(\w+)$", r"^<a>/b/(\w+)$"),
    (r"^(?P<a>\w+)/b/(?P<c>\w+)/$", r"^<a>/b/<c>/$"),
    (r"^(?P<group1>\d{2})-(?P<group2>\d{2})$", r"^<group1>-<group2>$"),
    (r"^(?P<code>(?P<subcode>\d+))$", r"^<code>$"),
    (r"^(?P<name>\w+)$", r"^<name>$"),
    (r"^(?P<first>\w+)\s+(?P<last>\w+)$", r"^<first>\s+<last>$"),
])
def test_replace_named_groups(pattern, expected):
    result = replace_named_groups(pattern)
    assert result == expected

def test_replace_named_groups_with_unmatched_groups():
    pattern = r"^(?P<name>\w+)(/b/(?P<id>\d+)|$"
    with pytest.raises(IndexError):
        replace_named_groups(pattern)

def test_replace_named_groups_with_nested_groups():
    pattern = r"^(?P<outer>(?P<inner>\d+))/b/$"
    expected = r"^<outer>/b/$"
    result = replace_named_groups(pattern)
    assert result == expected