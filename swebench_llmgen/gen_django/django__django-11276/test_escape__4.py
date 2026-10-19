import pytest
from django.utils.html import escape

def test_escape():
    # Test escaping of special HTML characters
    assert escape('<script>') == '&lt;script&gt;'
    assert escape('&') == '&amp;'
    assert escape('"') == '&quot;'
    assert escape("'") == '&#x27;'
    assert escape('>') == '&gt;'
    
    # Test escaping already escaped characters
    assert escape('&amp;') == '&amp;amp;'
    assert escape('&lt;') == '&amp;lt;'
    assert escape('&gt;') == '&amp;gt;'
    assert escape('&quot;') == '&amp;quot;'
    
    # Test escaping of plain text
    assert escape('Hello, World!') == 'Hello, World!'
    
    # Test escaping of multiple characters
    assert escape('<div>"Hello & <World></div>') == '&lt;div&gt;&quot;Hello &amp; &lt;World&gt;&lt;/div&gt;'
    
    # Test escaping of empty string
    assert escape('') == ''
    
    # Test escaping of special characters with spaces
    assert escape('Hello & Goodbye <World>') == 'Hello &amp; Goodbye &lt;World&gt;'