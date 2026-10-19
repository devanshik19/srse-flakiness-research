import pytest
from django.utils.html import escape
from django.template.defaultfilters import escape_filter

@pytest.mark.parametrize("input_value, expected_output", [
    ("<div>Hello</div>", "&lt;div&gt;Hello&lt;/div&gt;"),
    ("Hello & World", "Hello &amp; World"),
    ("<script>alert('XSS')</script>", "&lt;script&gt;alert('XSS')&lt;/script&gt;"),
    ("Normal text", "Normal text"),
    (None, ""),
])
def test_escape_filter(input_value, expected_output):
    if input_value is None:
        result = escape_filter(input_value)
    else:
        result = escape_filter(input_value)
    
    assert result == expected_output