import pytest
from django.utils.html import escapejs
from django.template.defaultfilters import escapejs_filter

def test_escapejs_filter():
    # Test with a standard string containing JavaScript characters
    input_value = "This is a test: \n ' \" \\ \u2028"
    expected_output = "This is a test: \\n \\u0027 \\u0022 \\\\ \\u2028"
    assert escapejs_filter(input_value) == expected_output

    # Test with an empty string
    assert escapejs_filter("") == ""

    # Test with a string containing only whitespace
    assert escapejs_filter("     ") == "     "

    # Test with a string of special characters
    special_chars = "!@#$%^&*()"
    assert escapejs_filter(special_chars) == special_chars

    # Test with a string containing unicode characters
    unicode_value = "Unicode test: \u2603 \u2665"
    expected_unicode_output = "Unicode test: \\u2603 \\u2665"
    assert escapejs_filter(unicode_value) == expected_unicode_output