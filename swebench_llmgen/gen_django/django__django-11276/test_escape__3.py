import pytest
from django.utils.html import escape

def test_escape():
    # Test basic escape of special characters
    assert escape('<script>') == '&lt;script&gt;'
    assert escape('&') == '&amp;'
    assert escape('"') == '&quot;'
    assert escape("'") == '&#x27;'
    assert escape('>') == '&gt;'
    
    # Test combination of characters
    assert escape('<div>"Hello & Welcome"</div>') == '&lt;div&gt;&quot;Hello &amp; Welcome&quot;&lt;/div&gt;'
    
    # Test double escaping
    assert escape('&lt;script&gt;') == '&amp;lt;script&amp;gt;'
    
    # Test with different types of input
    assert escape(None) == 'None'
    assert escape('plain text') == 'plain text'
    assert escape('') == ''
    
    # Test with SafeString input
    from django.utils.safestring import mark_safe
    safe_text = mark_safe('<b>bold</b>')
    assert escape(safe_text) == '&lt;b&gt;bold&lt;/b&gt;'