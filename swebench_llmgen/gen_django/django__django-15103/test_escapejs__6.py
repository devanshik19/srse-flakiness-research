import pytest
from django.utils.html import escapejs

@pytest.mark.parametrize("input_value, expected_output", [
    ("Hello, World!", "Hello, World!"),
    ("Newline:\nTab:\t", "Newline:\nTab:\t"),
    ("Special characters: ' \" \\", "Special characters: &#x27; &quot; &#x5C;"),
    ("Non-ASCII: ñ", "Non-ASCII: ñ"),
    ("<script>alert('XSS')</script>", "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"),
])
def test_escapejs(input_value, expected_output):
    assert escapejs(input_value) == expected_output