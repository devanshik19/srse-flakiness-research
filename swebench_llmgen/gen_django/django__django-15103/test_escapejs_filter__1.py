import pytest
from django.template.defaultfilters import escapejs_filter

def test_escapejs_filter():
    # Test with a simple string
    assert escapejs_filter("Hello, World!") == "Hello, World!"
    
    # Test with special characters
    assert escapejs_filter("Quotes: ' \" \\ /") == "Quotes: ' \" \\\\ /"
    
    # Test with a string containing a newline
    assert escapejs_filter("New\nLine") == "New\\nLine"
    
    # Test with control characters
    assert escapejs_filter("Control char: \x00") == "Control char: \\u0000"
    
    # Test with a string that only contains whitespace
    assert escapejs_filter("    ") == "    "
    
    # Test with an empty string
    assert escapejs_filter("") == ""
    
    # Test with a Unicode character
    assert escapejs_filter("Unicode: 😊") == "Unicode: 😊"