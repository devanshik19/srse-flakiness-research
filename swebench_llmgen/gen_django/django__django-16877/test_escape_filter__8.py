import pytest
from django.utils.html import conditional_escape
from django.template.defaultfilters import escape_filter

def test_escape_filter():
    # Test with a simple string
    value = '<script>alert("test")</script>'
    expected = conditional_escape(value)
    assert escape_filter(value) == expected

    # Test with normal text
    value = 'Hello World!'
    expected = conditional_escape(value)
    assert escape_filter(value) == expected

    # Test with HTML entities
    value = '5 > 3 & 2 < 4'
    expected = conditional_escape(value)
    assert escape_filter(value) == expected

    # Test with an empty string
    value = ''
    expected = conditional_escape(value)
    assert escape_filter(value) == expected

    # Test with a string containing special characters
    value = '© 2023 Company'
    expected = conditional_escape(value)
    assert escape_filter(value) == expected
    
    # Test with strings containing single quotes
    value = "It's a test."
    expected = conditional_escape(value)
    assert escape_filter(value) == expected
    
    # Test with strings containing double quotes
    value = '"Quoted" text'
    expected = conditional_escape(value)
    assert escape_filter(value) == expected