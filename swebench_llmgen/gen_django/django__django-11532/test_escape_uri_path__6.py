import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test with a simple path containing no unsafe characters
    assert escape_uri_path('/path/to/resource') == '/path/to/resource'

    # Test with reserved characters
    assert escape_uri_path('/path/to/resource?query=1') == '/path/to/resource%3Fquery%3D1'
    assert escape_uri_path('/path/to/resource&param=2') == '/path/to/resource&param=2'
    
    # Test with unsafe characters
    assert escape_uri_path('/path/to/resource#fragment') == '/path/to/resource%23fragment'
    assert escape_uri_path('/path/to/resource;params') == '/path/to/resource%3Bparams'
    
    # Test with mixed characters
    assert escape_uri_path('/path/to/resource!@#$%^&*()') == '/path/to/resource!@%23%24%25%5E%26%2A%28%29'
    
    # Test with spaces and special characters
    assert escape_uri_path('/path/to resource') == '/path/to%20resource'
    assert escape_uri_path('/path/to/resource with spaces') == '/path/to/resource%20with%20spaces'
    
    # Test with an empty path
    assert escape_uri_path('') == ''