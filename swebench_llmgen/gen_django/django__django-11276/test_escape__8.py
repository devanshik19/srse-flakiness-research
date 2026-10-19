import pytest
from django.utils.html import escape

def test_escape():
    # Test escaping of basic HTML characters
    assert escape('<div>') == '&lt;div&gt;'
    assert escape('&') == '&amp;'
    assert escape('"') == '&quot;'
    assert escape("'") == '&#x27;'  # Single quote
    assert escape('>') == '&gt;'
    
    # Test escaping of already escaped characters (double escaping)
    assert escape('&lt;div&gt;') == '&lt;div&gt;'
    assert escape('&amp;') == '&amp;'
    
    # Test escaping of plain text
    assert escape('Hello, World!') == 'Hello, World!'
    
    # Test escaping of text with multiple characters
    test_string = '<script>alert("XSS")</script>'
    expected_output = '&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;'
    assert escape(test_string) == expected_output
    
    # Test escaping an empty string
    assert escape('') == ''

    # Test escaping non-string types
    assert escape(123) == '123'
    assert escape(3.14) == '3.14'
    assert escape(None) == 'None'