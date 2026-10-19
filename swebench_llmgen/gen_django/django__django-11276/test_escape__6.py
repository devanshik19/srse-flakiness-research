import pytest
from django.utils.html import escape

def test_escape():
    # Test basic HTML escaping
    assert escape('<div>') == '&lt;div&gt;'
    assert escape('&') == '&amp;'
    assert escape('"') == '&quot;'
    assert escape("'") == '&#39;'
    
    # Test escaping with already escaped input
    assert escape('&lt;div&gt;') == '&amp;lt;div&amp;gt;'
    assert escape('&quot;hello&quot;') == '&amp;quot;hello&amp;quot;'
    
    # Test escaping special characters
    assert escape('Hello & welcome to <Django>!') == 'Hello &amp; welcome to &lt;Django&gt;!'
    
    # Test escaping an empty string
    assert escape('') == ''
    
    # Test escaping whitespace
    assert escape(' ') == ' '
    
    # Test escaping a string with no special characters
    assert escape('Hello World') == 'Hello World'