import pytest
from django.utils.html import escapejs

@pytest.mark.parametrize("input_value, expected_output", [
    ("Hello, World!", "Hello, World!"),
    ("'Quotes'", "'Quotes'"),
    ("\"Double Quotes\"", "\"Double Quotes\""),
    ("Backslash \\ and newline \n character", "Backslash \\\\ and newline \\n character"),
    ("Special chars: \u2018\u2019\u201c\u201d", "Special chars: \u2018\u2019\u201c\u201d"),
    ("<script>alert('XSS');</script>", "<script>alert('XSS');</script>")
])
def test_escapejs(input_value, expected_output):
    assert escapejs(input_value) == expected_output