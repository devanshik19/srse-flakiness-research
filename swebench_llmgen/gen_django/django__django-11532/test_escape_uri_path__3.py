import pytest
from django.utils.encoding import escape_uri_path

def test_escape_uri_path():
    # Test with a normal string containing reserved characters
    assert escape_uri_path("a b c") == "a%20b%20c"
    assert escape_uri_path("hello/world") == "hello/world"
    assert escape_uri_path("path:with?query=string&other=params") == "path:with%3Fquery%3Dstring%26other%3Dparams"
    
    # Test with special characters that need escaping
    assert escape_uri_path("~!@#$%^&*()") == "~!@#$%^&*()"
    assert escape_uri_path("this&that=other") == "this&that=other"
    
    # Test with empty string
    assert escape_uri_path("") == ""

    # Test with a string that only consists of unsafe characters
    assert escape_uri_path(";:,") == "%3B%3A%2C"
    
    # Test with a string that contains all unsafe characters
    assert escape_uri_path(":/@&+$,-_.!~*'()") == "safe:path/"