import pytest
from django.utils.html import escape

def test_escape():
    # Test basic HTML characters
    assert escape("<div>") == "&lt;div&gt;"
    assert escape("</>") == "&lt;/&gt;"
    assert escape("&") == "&amp;"
    assert escape('"') == "&quot;"
    assert escape("'") == "&#x27;"
    
    # Test mixed content
    assert escape('Hello <World> & "Python"') == 'Hello &lt;World&gt; &amp; &quot;Python&quot;'

    # Test already escaped content (double-escaping)
    assert escape('&lt;div&gt;') == '&amp;lt;div&amp;gt;'
    
    # Test plaintext input
    assert escape('Just some plain text.') == 'Just some plain text.'

    # Test empty input
    assert escape('') == ''
    
    # Test special unicode characters
    assert escape('© 2023') == '© 2023'

    # Test escape content with leading/trailing whitespace
    assert escape('  <test>  ') == '  &lt;test&gt;  '