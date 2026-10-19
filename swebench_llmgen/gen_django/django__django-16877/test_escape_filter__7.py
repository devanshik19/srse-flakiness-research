import pytest
from django.utils.html import escape
from django.template.defaultfilters import escape_filter

def test_escape_filter():
    # Test with a normal string
    value = "<script>alert('test');</script>"
    expected_output = escape(value)
    assert escape_filter(value) == expected_output

    # Test with an empty string
    value = ""
    expected_output = escape(value)
    assert escape_filter(value) == expected_output

    # Test with a string containing no HTML
    value = "Just a plain string"
    expected_output = escape(value)
    assert escape_filter(value) == expected_output

    # Test with a string containing special HTML characters
    value = "Some & special <characters> to escape"
    expected_output = escape(value)
    assert escape_filter(value) == expected_output

    # Test with a string containing quotes
    value = '"Quotes" and \'apostrophes\' should be escaped'
    expected_output = escape(value)
    assert escape_filter(value) == expected_output