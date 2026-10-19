import pytest
from django.utils.html import escape

def test_escape():
    # Test escaping of common HTML characters
    assert escape("<div>") == "&lt;div&gt;"
    assert escape("&") == "&amp;"
    assert escape('"') == "&quot;"
    assert escape("'") == "&#x27;"  # Single quote (apostrophe) can be HTML encoded as well
    assert escape(">") == "&gt;"

    # Test escaping of already escaped characters
    assert escape("&amp;") == "&amp;amp;"
    assert escape("&lt;div&gt;") == "&amp;lt;div&amp;gt;"

    # Test with non-HTML characters
    assert escape("Hello, World!") == "Hello, World!"

    # Test with whitespace content
    assert escape("    ") == "    "

    # Test with empty string
    assert escape("") == ""

    # Test with HTML and non-HTML mix
    assert escape("Hello <b>World</b> & Friends") == "Hello &lt;b&gt;World&lt;/b&gt; &amp; Friends"