import pytest
from django.contrib.admindocs.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases for replace_unnamed_groups function
    test_cases = [
        {
            "input": r"^(?P<a>\w+)/b/(\w+)$",
            "expected": r"^(?P<a>\w+)/b/<var>$"
        },
        {
            "input": r"^(?P<a>\w+)/b/((x|y)\w+)$",
            "expected": r"^(?P<a>\w+)/b/<var>$"
        },
        {
            "input": r"^(?P<a>\w+)/(b|c)/(\d+)$",
            "expected": r"^(?P<a>\w+)/(b|c)/<var>$"
        },
        {
            "input": r"^/path/(?P<name>\w+)$",
            "expected": r"^/path/(?P<name>\w+)$"
        },
        {
            "input": r"Single unnamed group: (\w+)$",
            "expected": r"Single unnamed group: <var>$"
        },
        {
            "input": r"Nested unnamed: ((\d+)[a-z]*)$",
            "expected": r"Nested unnamed: <var>$"
        },
        {
            "input": r"No groups here",
            "expected": r"No groups here"
        }
    ]

    for case in test_cases:
        result = replace_unnamed_groups(case["input"])
        assert result == case["expected"], f"Expected {case['expected']} but got {result} for input {case['input']}"