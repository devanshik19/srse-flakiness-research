import pytest
from django.utils.html import escape
from django.template.defaultfilters import escape_filter

@pytest.mark.parametrize("input_value, expected_output", [
    ("<div>Hello</div>", "&lt;div&gt;Hello&lt;/div&gt;"),
    ("&", "&amp;"),
    ("'Quotes'", "&#x27;Quotes&#x27;"),
    ('"Double Quotes"', '&#x22;Double Quotes&#x22;'),
    ("Hello World!", "Hello World!"),
    ("<script>alert('XSS')</script>", "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"),
    (None, ""),
])
def test_escape_filter(input_value, expected_output):
    assert escape_filter(input_value) == expected_output