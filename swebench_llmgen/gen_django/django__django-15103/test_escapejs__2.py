import pytest
from django.utils.html import escapejs
from django.utils.safestring import SafeString

@pytest.mark.parametrize("input_value, expected_output", [
    ("hello", SafeString("hello")),
    ("double quote \"", SafeString("double quote \\\"")),
    ("single quote '", SafeString("single quote \\'")),
    ("backslash \\ ", SafeString("backslash \\\\ ")),
    ("new line \n", SafeString("new line \\n")),
    ("tab \t", SafeString("tab \\t")),
    ("alert('XSS')", SafeString("alert(\'XSS\')")),
])
def test_escapejs(input_value, expected_output):
    result = escapejs(input_value)
    assert result == expected_output