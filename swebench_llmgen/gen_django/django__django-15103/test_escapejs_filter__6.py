import pytest
from django.template.defaultfilters import escapejs_filter

@pytest.mark.parametrize("test_input, expected_output", [
    ("Hello, World!", "Hello, World!"),
    ("JavaScript alert('Hello!');", "JavaScript alert('Hello!');"),
    ("A test with a newline\ncharacter.", "A test with a newline\\ncharacter."),
    ("Unsafe <script> tags & symbols: ©, ™, °", "Unsafe \\u003Cscript\\u003E tags & symbols: \\u00A9, \\u2122, \\u00B0"),
    ("Quotes: 'single' and \"double\"", "Quotes: \\u0027single\\u0027 and \\u0022double\\u0022"),
])

def test_escapejs_filter(test_input, expected_output):
    result = escapejs_filter(test_input)
    assert result == expected_output