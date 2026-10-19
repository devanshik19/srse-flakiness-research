import pytest
from django.utils.html import escape

def test_escape():
    # Test escaping different types of input
    
    # Test basic HTML characters
    assert escape("<div>") == "&lt;div&gt;"
    assert escape("&") == "&amp;"
    assert escape('"') == "&quot;"
    assert escape("'") == "&#39;"
    
    # Test a string that is already escaped
    assert escape("&lt;div&gt;") == "&amp;lt;div&amp;gt;"
    
    # Test no escaping (just return the same string)
    assert escape("") == ""
    assert escape("normal text") == "normal text"
    
    # Test escaping special characters combination
    assert escape("It's 100% safe!") == "It&#39;s 100% safe!"
    
    # Test long strings
    long_string = "<p>" + "test " * 1000 + "</p>"
    expected_output = "&lt;p&gt;" + "test " * 1000 + "&lt;/p&gt;"
    assert escape(long_string) == expected_output
    
    # Test numbers and white spaces
    assert escape("123") == "123"
    assert escape("   ") == "   "