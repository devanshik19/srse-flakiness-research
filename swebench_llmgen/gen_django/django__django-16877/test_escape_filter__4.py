import pytest
from django.utils.html import conditional_escape
from django.template.defaultfilters import escape_filter

def test_escape_filter():
    # Test regular string
    input_value = "<script>alert('XSS')</script>"
    expected_output = conditional_escape(input_value)
    assert escape_filter(input_value) == expected_output
    
    # Test with HTML special characters
    input_value = "Tom & Jerry"
    expected_output = conditional_escape(input_value)
    assert escape_filter(input_value) == expected_output
    
    # Test with a safe string
    input_value = mark_safe("<strong>Safe String</strong>")
    assert escape_filter(input_value) == expected_output  # Should remain the same as it is safe

    # Test with None input
    input_value = None
    expected_output = ''
    assert escape_filter(input_value) == expected_output
    
    # Test with empty string
    input_value = ""
    expected_output = ''
    assert escape_filter(input_value) == expected_output