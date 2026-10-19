import pytest
from django.utils.html import conditional_escape
from django.template.defaultfilters import escape_filter

@pytest.mark.parametrize("input_value, expected_output", [
    ("<script>alert('XSS')</script>", "&lt;script&gt;alert('XSS')&lt;/script&gt;"),
    ("&", "&amp;"),
    ("<div>Hello</div>", "&lt;div&gt;Hello&lt;/div&gt;"),
    ("Normal Text", "Normal Text"),
    ("", ""),
    ("'single quotes'", "'single quotes'"),
    ("\"double quotes\"", "\"double quotes\""),
])
def test_escape_filter(input_value, expected_output):
    result = escape_filter(input_value)
    assert result == expected_output
    assert result == conditional_escape(input_value)