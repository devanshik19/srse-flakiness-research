import pytest
from django.utils.html import escapejs
from django.template.defaultfilters import escapejs_filter

@pytest.mark.parametrize("value, expected", [
    ("string with 'quotes' and \\backslashes\\", "string with \u0027quotes\u0027 and \u005Cbackslashes\u005C"),
    ("<script>alert('XSS');</script>", "\u003Cscript\u003Ealert(\u0027XSS\u0027);\u003C/script\u003E"),
    ("Normal text", "Normal text"),
    ("'Single quotes'", "\u0027Single quotes\u0027"),
    ("\"Double quotes\"", "\u0022Double quotes\u0022"),
    ("Newline\n", "Newline\u000A"),
])
def test_escapejs_filter(value, expected):
    assert escapejs_filter(value) == expected