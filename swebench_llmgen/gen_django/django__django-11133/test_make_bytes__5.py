import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:
    
    @pytest.fixture
    def response(self):
        return HttpResponseBase(content_type='text/plain', status=200, reason='OK', charset='utf-8')

    def test_make_bytes_with_bytes(self, response):
        value = b'test bytes'
        result = response.make_bytes(value)
        assert result == value
        assert isinstance(result, bytes)

    def test_make_bytes_with_str(self, response):
        value = 'test string'
        result = response.make_bytes(value)
        assert result == b'test string'
        assert isinstance(result, bytes)

    def test_make_bytes_with_non_string(self, response):
        value = 123
        result = response.make_bytes(value)
        assert result == b'123'
        assert isinstance(result, bytes)

    def test_make_bytes_with_empty_string(self, response):
        value = ''
        result = response.make_bytes(value)
        assert result == b''
        assert isinstance(result, bytes)

    def test_make_bytes_with_bytes_subclass(self, response):
        class CustomBytes(bytes):
            pass
        
        value = CustomBytes(b'test subclass')
        result = response.make_bytes(value)
        assert result == value
        assert isinstance(result, bytes)
    
    def test_make_bytes_with_different_charset(self, response):
        response.charset = 'latin-1'
        value = 'éclair'
        result = response.make_bytes(value)
        assert result == b'\xe9clair'
        assert isinstance(result, bytes)