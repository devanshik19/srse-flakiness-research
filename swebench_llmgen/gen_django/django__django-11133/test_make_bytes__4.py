import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:

    @pytest.fixture
    def http_response(self):
        return HttpResponseBase(content_type='text/plain', status=200, reason='OK', charset='utf-8')

    def test_make_bytes_with_bytes(self, http_response):
        value = b'some bytes'
        result = http_response.make_bytes(value)
        assert result == value  # Should return bytes without modification

    def test_make_bytes_with_string(self, http_response):
        value = 'some string'
        result = http_response.make_bytes(value)
        assert result == b'some string'  # Should return bytes encoded with the charset

    def test_make_bytes_with_non_string(self, http_response):
        value = 12345  # Non-string type
        result = http_response.make_bytes(value)
        assert result == b'12345'  # Should convert non-string to string and then to bytes

    def test_make_bytes_with_utf8_string(self, http_response):
        value = '你好'
        result = http_response.make_bytes(value)
        assert result == b'\xe4\xbd\xa0\xe5\xa5\xbd'  # Validate the UTF-8 encoding result

    def test_make_bytes_with_empty_string(self, http_response):
        value = ''
        result = http_response.make_bytes(value)
        assert result == b''  # Should handle empty string correctly