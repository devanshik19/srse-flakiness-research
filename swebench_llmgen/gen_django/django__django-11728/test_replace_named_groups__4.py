import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

@pytest.mark.parametrize("input_pattern, expected_output", [
    (r"^(?P<a>\w+)/b/(\w+)$", r"^<a>/b/(\w+)$"),
    (r"^(?P<a>\w+)/b/(?P<c>\w+)/$", r"^<a>/b/<c>/$"),
    (r"^(?P<a>\w+)/b/(?P<c>(\w+))/(?P<d>\d+)/$", r"^<a>/b/<c>/<d>/$"),
    (r"^(?P<first>\w+)(?P<second>\w+)$", r"^<first><second>$"),
    (r"^(?P<outer>(?P<nested>foo|bar))/test$", r"^<outer>/test$"),
    (r"^(?P<empty>(?P<inner>\w+))$", r"^<empty>$"),
    (r"^/path/(?P<param>\d+)$", r"^/path/<param>$"),
    (r"^(?P<name>\w+)/$", r"^<name>/$"),
    (r"abc", r"abc")  # No named groups present
])
def test_replace_named_groups(input_pattern, expected_output):
    assert replace_named_groups(input_pattern) == expected_output

def test_replace_named_groups_no_named_groups():
    assert replace_named_groups("simple/path") == "simple/path"

def test_replace_named_groups_multiple_nested_groups():
    pattern = r"^(?P<outer>(?P<inner>\w+))/b/(?P<param>\w+)$"
    expected = r"^<outer>/b/<param>$"
    assert replace_named_groups(pattern) == expected