import pytest
from django.utils.html import escape

def test_escape():
    # Test escaping of HTML characters
    assert escape("<div>") == "&lt;div&gt;"
    assert escape("</script>") == "&lt;/script&gt;"
    assert escape("&") == "&amp;"
    assert escape('"') == "&quot;"
    assert escape("'") == "&#39;"
    
    # Test with already escaped string
    assert escape("&lt;p&gt;Hello World!&lt;/p&gt;") == "&amp;lt;p&amp;gt;Hello World!&amp;lt;/p&amp;gt;"

    # Test with normal string
    assert escape("Hello & welcome to <Django>!") == "Hello &amp; welcome to &lt;Django&gt;!"
    
    # Test with empty string
    assert escape("") == ""
    
    # Test with non-string input
    assert escape(123) == "123"
    assert escape(45.67) == "45.67"