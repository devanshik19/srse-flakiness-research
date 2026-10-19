import pytest
from django.utils.html import escape
from django.template.defaultfilters import escape_filter

def test_escape_filter():
    # Test with normal string
    normal_string = "<div>Hello World</div>"
    escaped_string = escape_filter(normal_string)
    assert escaped_string == escape(normal_string)

    # Test with unsafe string containing HTML
    unsafe_string = '<script>alert("XSS")</script>'
    escaped_unsafe_string = escape_filter(unsafe_string)
    assert escaped_unsafe_string == escape(unsafe_string)

    # Test with an empty string
    empty_string = ""
    escaped_empty_string = escape_filter(empty_string)
    assert escaped_empty_string == escape(empty_string)

    # Test with safe string (should remain unchanged)
    safe_string = mark_safe("<strong>This is safe</strong>")
    escaped_safe_string = escape_filter(safe_string)
    assert escaped_safe_string == safe_string

    # Test with non-string input (should be converted to string and then escaped)
    non_string_input = 12345
    escaped_non_string = escape_filter(non_string_input)
    assert escaped_non_string == escape(str(non_string_input))