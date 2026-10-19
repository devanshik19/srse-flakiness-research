import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test with a normal path
    assert escape_uri_path("/path/to/resource") == "/path/to/resource"
    
    # Test with unsafe characters
    assert escape_uri_path("/path/?query=example&other=unsafe#fragment") == "/path/%3Fquery%3Dexample%26other%3Dunsafe%23fragment"
    
    # Test with reserved characters
    assert escape_uri_path("/path/to/;params?query=example") == "/path/to/;params%3Fquery%3Dexample"

    # Test with a completely unsafe string
    assert escape_uri_path("unsafe characters: !$&'()*+,/:;=?@") == "unsafe%20characters%3A%20%21%24%26%27%28%29%2A%2B%2C%2F%3A%3B%3D%3F%40"
    
    # Test with empty path
    assert escape_uri_path("") == ""
    
    # Test with space
    assert escape_uri_path("path with spaces") == "path%20with%20spaces"
    
    # Test with Unicode characters
    assert escape_uri_path("path/with/unicode/😃") == "path/with/unicode/%F0%9F%98%83"