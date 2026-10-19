import pytest
from django.utils.encoding import escape_uri_path

@pytest.mark.parametrize("input_path, expected_output", [
    ("/path/to/resource", "/path/to/resource"),
    ("/path/to/resource?query=string", "/path/to/resource?query=string"),
    ("/path/to/resource&other=value", "/path/to/resource&other=value"),
    ("unsafe chars: !@#$%^&*()", "unsafe%20chars%3A%20%21%40%23%24%25%5E%26%2A%28%29"),
    ("another/example/path/with/slash/", "another/example/path/with/slash/"),
    ("regular-path_with-dashes_and.dots", "regular-path_with-dashes_and.dots"),
    ("path/with spaces", "path/with%20spaces"),
    ("path/with+plus", "path/with%2Bplus"),
    ("path/with$sign", "path/with%24sign"),
    ("path/with,comma", "path/with%2Ccomma"),
    ("path/with'quote", "path/with%27quote"),
    ("path/with(parentheses)", "path/with%28parentheses%29"),
])
def test_escape_uri_path(input_path, expected_output):
    assert escape_uri_path(input_path) == expected_output