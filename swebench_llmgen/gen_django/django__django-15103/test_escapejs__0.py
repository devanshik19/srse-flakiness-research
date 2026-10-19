import pytest
from django.utils.html import escapejs

@pytest.mark.parametrize("value, expected", [
    ("Hello, world!", "Hello, world!"),
    ("This is a test: <, >, &, '\"", "This is a test: \\u003C, \\u003E, \\u0026, \\u0027\\u0022"),
    ("Newline\nTab\t", "Newline\\u000ATab\\u0009"),
    ("Unicode: ß, €, ™", "Unicode: \\u00DF, \\u20AC, \\u2122"),
    ("Quotes: ' \"", "Quotes: \\u0027 \\u0022"),
    ("Backslash: \\", "Backslash: \\\\"),
])
def test_escapejs(value, expected):
    result = escapejs(value)
    assert result == expected