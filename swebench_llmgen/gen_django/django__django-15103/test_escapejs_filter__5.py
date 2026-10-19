import pytest
from django.utils.html import escapejs
from django.template.defaultfilters import escapejs_filter

@pytest.mark.parametrize("input_value,expected_output", [
    ("Hello World", "Hello World"),  # Normal string
    ("\"Single Quote' & < >", "\"Single Quote' & < >"),  # Special characters
    ("Backslash: \\", "Backslash: \\"),  # Backslash
    ("Unicode: Ø", "Unicode: Ø"),  # Unicode character
    ("Line\nBreak", "Line\\nBreak"),  # Newline character
    ("Tab\tCharacter", "Tab\\tCharacter"),  # Tab character
])
def test_escapejs_filter(input_value, expected_output):
    assert escapejs_filter(input_value) == expected_output