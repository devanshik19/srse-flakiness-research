import pytest
from django.utils.html import escape
from django.template.defaultfilters import escape_filter

def test_escape_filter():
    # Test normal string input
    input_value = "<script>alert('test')</script>"
    expected_output = escape(input_value)
    assert escape_filter(input_value) == expected_output

    # Test empty string
    input_value = ""
    expected_output = escape(input_value)
    assert escape_filter(input_value) == expected_output

    # Test string with HTML entities
    input_value = "This & that"
    expected_output = escape(input_value)
    assert escape_filter(input_value) == expected_output

    # Test string with multiple escaped characters
    input_value = "A < b > c & d ' e \" f"
    expected_output = escape(input_value)
    assert escape_filter(input_value) == expected_output

    # Test string with only whitespace
    input_value = "    "
    expected_output = escape(input_value)
    assert escape_filter(input_value) == expected_output

    # Test string with no HTML content
    input_value = "Just a plain text"
    expected_output = escape(input_value)
    assert escape_filter(input_value) == expected_output