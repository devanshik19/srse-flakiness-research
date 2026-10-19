import pytest
from django.utils.html import conditional_escape
from django.template.defaultfilters import escape_filter

def test_escape_filter():
    # Test with a normal string
    normal_string = "<div>Hello, World!</div>"
    expected_output = conditional_escape(normal_string)
    assert escape_filter(normal_string) == expected_output

    # Test with an empty string
    empty_string = ""
    assert escape_filter(empty_string) == ""

    # Test with a string containing special HTML characters
    special_string = "<script>alert('xss');</script>"
    expected_output = conditional_escape(special_string)
    assert escape_filter(special_string) == expected_output

    # Test with a string that includes quotes
    quotes_string = 'He said, "Hello!"'
    expected_output = conditional_escape(quotes_string)
    assert escape_filter(quotes_string) == expected_output

    # Test with a string that includes single quotes
    single_quote_string = "It's a sunny day."
    expected_output = conditional_escape(single_quote_string)
    assert escape_filter(single_quote_string) == expected_output