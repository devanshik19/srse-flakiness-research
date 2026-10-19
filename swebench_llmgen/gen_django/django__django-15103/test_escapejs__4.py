import pytest
from django.utils.html import escapejs
from django.utils.safestring import mark_safe

def test_escapejs():
    # Test normal string
    assert escapejs("Hello World") == mark_safe("Hello World")
    
    # Test string with special characters
    assert escapejs("\"'\\") == mark_safe("\\u0022\\u0027\\u005C")
    
    # Test string with newline
    assert escapejs("Hello\nWorld") == mark_safe("Hello\\u000AWorld")
    
    # Test string with a unicode character
    assert escapejs("Hello 😊") == mark_safe("Hello \\uD83D\\uDE0A")
    
    # Test string with various special characters
    assert escapejs("Escaped: \n\r\t\b\f\\\"\'") == mark_safe("Escaped: \\u000A\\u000D\\u0009\\u0008\\u000C\\u005C\\u0022\\u0027")
    
    # Test empty string
    assert escapejs("") == mark_safe("")