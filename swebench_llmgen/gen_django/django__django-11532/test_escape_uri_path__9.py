import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test cases with various input paths
    assert escape_uri_path("test/path") == "test/path"
    assert escape_uri_path("test/path with spaces") == "test/path%20with%20spaces"
    assert escape_uri_path("test/path?query=1") == "test/path/query=1"
    assert escape_uri_path("test/path&other=2") == "test/path&other=2"
    assert escape_uri_path("test/path:with:colons") == "test/path:with:colons"
    assert escape_uri_path("test/path@with@at") == "test/path@with@at"
    assert escape_uri_path("test/path#with#hash") == "test/path#with#hash"
    assert escape_uri_path("test/unsafe_chars!~*'()") == "test/unsafe_chars!~*'()"
    assert escape_uri_path("test/path;and;more") == "test/path;and;more"
    assert escape_uri_path("test/UNRESERVED_$%") == "test/UNRESERVED_$%"

    # Edge case with empty string
    assert escape_uri_path("") == ""