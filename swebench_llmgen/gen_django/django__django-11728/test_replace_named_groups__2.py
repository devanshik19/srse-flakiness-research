import pytest
import re
from email.errors import HeaderParseError
from email.parser import HeaderParser
from django.urls import reverse
from django.utils.safestring import mark_safe

def replace_named_groups(pattern):
    r"""
    Find named groups in `pattern` and replace them with the group name. E.g.,
    1. ^(?P<a>\w+)/b/(\w+)$ ==> ^<a>/b/(\w+)$
    2. ^(?P<a>\w+)/b/(?P<c>\w+)/$ ==> ^<a>/b/<c>/$
    """
    named_group_indices = [
        (m.start(0), m.end(0), m.group(1))
        for m in named_group_matcher.finditer(pattern)
    ]
    # Tuples of (named capture group pattern, group name).
    group_pattern_and_name = []
    # Loop over the groups and their start and end indices.
    for start, end, group_name in named_group_indices:
        # Handle nested parentheses, e.g. '^(?P<a>(x|y))/b'.
        unmatched_open_brackets, prev_char = 1, None
        for idx, val in enumerate(pattern[end:]):
            # If brackets are balanced, the end of the string for the current
            # named capture group pattern has been reached.
            if unmatched_open_brackets == 0:
                group_pattern_and_name.append((pattern[start:end + idx], group_name))
                break

            # Check for unescaped `(` and `)`. They mark the start and end of a
            # nested group.
            if val == '(' and prev_char != '\\':
                unmatched_open_brackets += 1
            elif val == ')' and prev_char != '\\':
                unmatched_open_brackets -= 1
            prev_char = val

    # Replace the string for named capture groups with their group names.
    for group_pattern, group_name in group_pattern_and_name:
        pattern = pattern.replace(group_pattern, group_name)
    return pattern

def test_replace_named_groups():
    # Test cases with expected outputs
    test_cases = [
        (r"^(?P<a>\w+)/b/(\w+)$", r"^<a>/b/(\w+)$"),
        (r"^(?P<a>\w+)/b/(?P<c>\w+)/$", r"^<a>/b/<c>/"),
        (r"^(?P<a>\w+)(?P<b>\d+)$", r"^<a><b>$"),
        (r"^(?P<id>\d+)(/detail/(?P<slug>[-\w]+))?$", r"^<id>(/detail/<slug>)?$"),
        (r"^(?P<foo>(\(\w+\)))$", r"^<foo>$"),
        (r"^(?P<bar>\w+)(\(\w+\))$", r"^<bar>(\(\w+\))$"),
        (r"^(?P<name>\w+)\s(?P<age>\d+)$", r"^<name> <age>$"),
    ]

    for pattern, expected in test_cases:
        assert replace_named_groups(pattern) == expected