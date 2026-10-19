import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test case with no special characters
    assert escape_uri_path('/simple/path') == '/simple/path'
    
    # Test case with reserved characters
    assert escape_uri_path('/path?query=value') == '/path?query=value'
    assert escape_uri_path('/path=value') == '/path=value'
    assert escape_uri_path('/path@here') == '/path@here'
    assert escape_uri_path('/path/with/slash') == '/path/with/slash'
    
    # Test case with unsafe characters
    assert escape_uri_path('/path with spaces') == '/path%20with%20spaces'
    assert escape_uri_path('/path#with#hashes') == '/path%23with%23hashes'
    assert escape_uri_path('/path%20with%20encoded') == '/path%20with%20encoded'
    
    # Test case with various special characters
    assert escape_uri_path('/path&symbol=and+plus') == '/path&symbol=and+plus'
    assert escape_uri_path('/path?name=John&Doe') == '/path?name=John&Doe'
    
    # Test case with mixed characters
    assert escape_uri_path('/Hello World!') == '/Hello%20World!'
    assert escape_uri_path('/test/123!@#%^&*()') == '/test/123!%40%23%25%5E%26%2A%28%29'