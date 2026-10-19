import pytest
from django.utils.html import escapejs
from django.template.defaultfilters import escapejs_filter

def test_escapejs_filter():
    # Test with normal string
    input_value = "Hello 'World' \"Test\""
    expected_output = escapejs(input_value)
    assert escapejs_filter(input_value) == expected_output

    # Test with special characters
    input_value = "<script>alert('Test');</script>"
    expected_output = escapejs(input_value)
    assert escapejs_filter(input_value) == expected_output

    # Test with empty string
    input_value = ""
    expected_output = escapejs(input_value)
    assert escapejs_filter(input_value) == expected_output

    # Test with space
    input_value = " "
    expected_output = escapejs(input_value)
    assert escapejs_filter(input_value) == expected_output

    # Test with unicode characters
    input_value = "Hello 😊"
    expected_output = escapejs(input_value)
    assert escapejs_filter(input_value) == expected_output

    # Test with a string containing only special characters
    input_value = "!@#$%^&*()"
    expected_output = escapejs(input_value)
    assert escapejs_filter(input_value) == expected_output