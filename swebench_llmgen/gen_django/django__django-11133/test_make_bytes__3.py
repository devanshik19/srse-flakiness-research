import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:
    @pytest.fixture
    def response(self):
        return HttpResponseBase(content_type='text/plain', status=200, reason='OK', charset='utf-8')

    def test_make_bytes_bytes_input(self, response):
        value = b'This is a byte string.'
        result = response.make_bytes(value)
        assert result == value
        assert isinstance(result, bytes)

    def test_make_bytes_str_input(self, response):
        value = 'This is a string.'
        result = response.make_bytes(value)
        assert result == b'This is a string.'
        assert isinstance(result, bytes)

    def test_make_bytes_non_string_input(self, response):
        value = 12345
        result = response.make_bytes(value)
        assert result == b'12345'
        assert isinstance(result, bytes)

    def test_make_bytes_non_string_utf8_input(self, response):
        value = 3.14
        result = response.make_bytes(value)
        assert result == b'3.14'
        assert isinstance(result, bytes)

    def test_make_bytes_empty_string(self, response):
        value = ''
        result = response.make_bytes(value)
        assert result == b''
        assert isinstance(result, bytes)