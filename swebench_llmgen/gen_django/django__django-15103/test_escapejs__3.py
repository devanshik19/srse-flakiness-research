import pytest
from django.utils.html import escapejs

@pytest.mark.parametrize("input_value, expected_output", [
    ("Hello World", "Hello World"),
    ("Single quote: '", "Single quote: \\u0027"),
    ("Double quote: \"", "Double quote: \\u0022"),
    ("Backslash: \\", "Backslash: \\\\"),
    ("Less than: <", "Less than: \\u003C"),
    ("Greater than: >", "Greater than: \\u003E"),
    ("Ampersand: &", "Ampersand: \\u0026"),
    ("Newline: \n", "Newline: \\n"),
    ("Tab: \t", "Tab: \\t"),
])

def test_escapejs(input_value, expected_output):
    assert escapejs(input_value) == expected_output