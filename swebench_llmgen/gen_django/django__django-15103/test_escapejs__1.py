import pytest
from django.utils.html import escapejs
from django.utils.safestring import SafeString

_js_escapes = str.maketrans({
    '\\': '\\\\',  # backslash
    "'": "\\'",    # single quote
    '"': '\\"',    # double quote
    '\n': '\\n',   # newline
    '\r': '\\r',   # carriage return
    '\t': '\\t',   # tab
})

@pytest.mark.parametrize("input_value, expected_output", [
    ("Hello 'world'", SafeString("Hello \\&#39;world&#39;")),
    ("Line1\nLine2", SafeString("Line1\\nLine2")),
    ("Quotes: \" \"", SafeString("Quotes: \\&quot; \\&quot;")),
    ("Backslash: \\", SafeString("Backslash: \\\\")),
    ("Escape: \tTabbed", SafeString("Escape: \\tTabbed")),
])
def test_escapejs(input_value, expected_output):
    result = escapejs(input_value)
    assert result == expected_output