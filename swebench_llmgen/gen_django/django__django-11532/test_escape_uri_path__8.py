import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test with a normal path
    assert escape_uri_path("/path/to/resource") == "/path/to/resource"
    
    # Test with reserved characters
    assert escape_uri_path("/path?query=1") == "/path%3Fquery%3D1"
    assert escape_uri_path("/path&other=value") == "/path%26other%3Dvalue"
    assert escape_uri_path("/path:value") == "/path%3Avalue"
    
    # Test with unsafe characters
    assert escape_uri_path("/path with spaces") == "/path%20with%20spaces"
    assert escape_uri_path("/path/with/!@#^&*()") == "/path/with/%21%40%23%5E%26%2A%28%29"
    
    # Test with empty path
    assert escape_uri_path("") == ""
    
    # Test with only safe characters
    assert escape_uri_path("safe-characters") == "safe-characters"

    # Test with combination of safe and unsafe characters
    assert escape_uri_path("unsafe@safe*chars") == "unsafe%40safe%2Achars"