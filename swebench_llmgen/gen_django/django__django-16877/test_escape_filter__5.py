import pytest
from django.utils.html import escape
from django.template.defaultfilters import escape_filter

def test_escape_filter():
    # Test with plain string
    assert escape_filter("<script>alert('xss')</script>") == escape("<script>alert('xss')</script>")

    # Test with string containing HTML
    assert escape_filter("<div>Content</div>") == escape("<div>Content</div>")
    
    # Test with string that does not need escaping
    assert escape_filter("Just plain text") == "Just plain text"
    
    # Test with string with special characters
    assert escape_filter("5 < 10 & 10 > 5") == escape("5 < 10 & 10 > 5")

    # Test with empty string
    assert escape_filter("") == ""

    # Test with None, should return empty string
    assert escape_filter(None) == ""