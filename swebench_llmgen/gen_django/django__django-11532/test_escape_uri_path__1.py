import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test escaping of unsafe characters in URI path
    assert escape_uri_path("path/to/resource") == "path/to/resource"
    assert escape_uri_path("path?query=string") == "path?query=string"
    assert escape_uri_path("path@domain.com") == "path@domain.com"
    assert escape_uri_path("path&another=value") == "path&another=value"
    assert escape_uri_path("unsafe;chars?") == "unsafe;chars?"
    assert escape_uri_path("hello world") == "hello%20world"
    assert escape_uri_path("string with / and ? and :") == "string%20with%20/%20and%20%3F%20and%20%3A"
    assert escape_uri_path("spaces   and   tabs\t") == "spaces%20%20%20and%20%20%20tabs%09"
    assert escape_uri_path("unreserved-_.!~*'()") == "unreserved-_.!~*'()"
    assert escape_uri_path("reserved:/@&+$,-_.!~*'()") == "reserved:/@&+$,-_.!~*'()"