import pytest
from django.utils.html import escapejs
from django.utils.safestring import SafeString

@pytest.mark.parametrize("input_value, expected_output", [
    ("Simple string", "Simple string"),
    ("String with quotes: \" and '", 'String with quotes: \u0022 and \u0027'),
    ("String with backslash: \\", 'String with backslash: \\u005c'),
    ("Special characters: \n and \t", 'Special characters: \\u000a and \\u0009'),
    ("Unicode: ñ", 'Unicode: ñ'),
    ("Emoji: 😊", 'Emoji: 😊'),
])
def test_escapejs(input_value, expected_output):
    result = escapejs(input_value)
    assert isinstance(result, SafeString)
    assert str(result) == expected_output