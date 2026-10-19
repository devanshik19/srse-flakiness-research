import pytest
import re
from django.contrib.admindocs.utils import replace_named_groups

# Pre-compile the regex pattern to simulate the `named_group_matcher` expected in the function.
named_group_matcher = re.compile(r'\(\?P<([a-zA-Z_][a-zA-Z0-9_]*)>')

@pytest.mark.parametrize(
    "pattern, expected",
    [
        (r'^(?P<a>\w+)/b/(\w+)$', r'^(<a>)/b/(\w+)$'),
        (r'^(?P<a>\w+)/b/(?P<c>\w+)/$', r'^(<a>)/b/(<c>)/$'),
        (r'^(?P<first>\d+)/(?P<second>\w+)/(foo|bar)$', r'^(<first>)/(<second>)/(foo|bar)$'),
        (r'^(?P<a>(x|y))/b/(?P<c>\w+)/$', r'^(<a>)/b/(<c>)/$'),
        (r'^(?P<group>\(nested\))/$', r'^(<group>)/$'),
        (r'^(?P<name1>\w+\d+)/(?P<name2>\d+)$', r'^(<name1>)/(<name2>)$'),
        (r'^/no/named/groups$', r'^/no/named/groups$')
    ]
)
def test_replace_named_groups(pattern, expected):
    assert replace_named_groups(pattern) == expected