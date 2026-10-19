import pytest
from django.utils.html import escapejs
from django.template.defaultfilters import escapejs_filter

@pytest.mark.parametrize("input_value, expected_output", [
    ("hello", "hello"),
    ("'hello'", r"\'hello\'"),
    ('"hello"', r'\"hello\"'),
    ("<script>alert('xss')</script>", r"<script>alert(\'xss\')<\/script>"),
    ("Café", "Caf\u00e9"),  # Testing Unicode character
    ("path/to/file", "path/to/file"),
    ("backslash\\test", "backslash\\\\test"),  # Escaping backslashes
])
def test_escapejs_filter(input_value, expected_output):
    assert escapejs_filter(input_value) == expected_output