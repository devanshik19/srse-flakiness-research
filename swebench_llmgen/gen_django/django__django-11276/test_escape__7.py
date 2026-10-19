import pytest
from django.utils.html import escape
from django.utils.safestring import SafeString

def test_escape():
    # Test cases with expected results
    test_cases = [
        ("<div>Test</div>", "&lt;div&gt;Test&lt;/div&gt;"),
        ('"Quote"', "&quot;Quote&quot;"),
        ("It's a test & example", "It&apos;s a test &amp; example"),
        ("Some text with <script>alert('XSS')</script>", "Some text with &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"),
        ('Already <b>escaped</b>', "Already &lt;b&gt;escaped&lt;/b&gt;"),
        ("Normal text", "Normal text"),
        ("", ""),
        (None, ""),
    ]
    
    for text, expected in test_cases:
        if text is None:
            result = escape(text)
        else:
            result = escape(text)
        assert result == expected
        assert isinstance(result, SafeString)