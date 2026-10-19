import pytest
from django.template.defaultfilters import escapejs_filter

@pytest.mark.parametrize("input_value,expected_output", [
    ("Hello, World!", "Hello, World!"),
    ("Quotes: \"Single\' and \'Double\"", "Quotes: \u0022Single\u0027 and \u0027Double\u0022"),
    ("Newline\nCharacter", "Newline\u000aCharacter"),
    ("Tab\tCharacter", "Tab\u0009Character"),
    ("Backslash\\Character", "Backslash\\Character"),
    ("Unicode 😃 Character", "Unicode \ud83d\ude03 Character"),
])
def test_escapejs_filter(input_value, expected_output):
    """Test the escapejs_filter function with different inputs."""
    assert escapejs_filter(input_value) == expected_output