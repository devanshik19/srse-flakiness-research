import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test with normal characters
    assert escape_uri_path("normal/path") == "normal/path"
    
    # Test with reserved characters
    assert escape_uri_path("path;params?query&name=value") == "path;params?query&name=value"
    
    # Test with unreserved characters
    assert escape_uri_path("safe-characters-_.!~*'()") == "safe-characters-_.!~*'()"
    
    # Test with spaces (should be escaped to %20)
    assert escape_uri_path("space in path") == "space%20in%20path"
    
    # Test with multiple special characters
    assert escape_uri_path("unsafe!#*<>@") == "unsafe%21%23%2A%3C%3E%40"
    
    # Test with empty string
    assert escape_uri_path("") == ""
    
    # Test with only unsafe characters
    assert escape_uri_path("!@#$%^&*()") == "%21%40%23%24%25%5E%26%2A%28%29"