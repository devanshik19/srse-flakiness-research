import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test with a simple path containing unsafe characters
    assert escape_uri_path('hello world') == 'hello%20world'
    assert escape_uri_path('foo/bar?baz=qux') == 'foo/bar?baz=qux'
    assert escape_uri_path('unsafe characters: @&+$,') == 'unsafe%20characters%3A%20%40%26%2B%24%2C'
    
    # Test with path including reserved and unreserved characters
    assert escape_uri_path('hello;world') == 'hello%3Bworld'
    assert escape_uri_path('/foo/bar/baz/') == '/foo/bar/baz/'
    
    # Test with empty string
    assert escape_uri_path('') == ''
    
    # Test with no unsafe characters
    assert escape_uri_path('abc-def_ghi.jkl!~*\'()') == 'abc-def_ghi.jkl!~*\'()'
    
    # Test with various escape needs
    assert escape_uri_path('http://example.com/foo?bar=baz') == 'http://example.com/foo?bar=baz'
    assert escape_uri_path('this/needs escaping!#') == 'this/needs%20escaping%21%23'