import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:
    
    def test_make_bytes_with_bytes(self):
        response = HttpResponseBase('text/plain', status=200, reason=None, charset='utf-8')
        result = response.make_bytes(b'Binary data')
        assert result == b'Binary data'
        assert isinstance(result, bytes)

    def test_make_bytes_with_string(self):
        response = HttpResponseBase('text/plain', status=200, reason=None, charset='utf-8')
        result = response.make_bytes('Test string')
        assert result == b'Test string'
        assert isinstance(result, bytes)

    def test_make_bytes_with_non_string(self):
        response = HttpResponseBase('text/plain', status=200, reason=None, charset='utf-8')
        result = response.make_bytes(123)
        assert result == b'123'
        assert isinstance(result, bytes)

    def test_make_bytes_with_none(self):
        response = HttpResponseBase('text/plain', status=200, reason=None, charset='utf-8')
        result = response.make_bytes(None)
        assert result == b'None'
        assert isinstance(result, bytes)