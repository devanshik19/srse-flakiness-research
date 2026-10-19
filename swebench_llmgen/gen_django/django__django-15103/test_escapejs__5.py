import pytest
from django.utils.html import escapejs

@pytest.mark.parametrize("value, expected", [
    ("simple string", "simple string"),
    ("string with \"quotes\"", "string with \\"quotes\\""),
    ("string with 'apostrophes'", "string with 'apostrophes'"),
    ("string with \\backslash", "string with \\\\backslash"),
    ("string with newline\ncharacter", "string with newline\\ncharacter"),
    ("string with tab\tcharacter", "string with tab\\tcharacter"),
    ("string with unicode \u2022 character", "string with unicode \\u2022 character"),
])
def test_escapejs(value, expected):
    result = escapejs(value)
    assert str(result) == expected