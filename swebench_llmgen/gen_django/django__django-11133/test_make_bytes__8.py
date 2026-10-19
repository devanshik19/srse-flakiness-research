import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:

    @pytest.fixture
    def response(self):
        return HttpResponseBase(content_type='text/plain', status=200, reason='OK', charset='utf-8')

    def test_make_bytes_with_bytes_input(self, response):
        value = b'test bytes'
        result = response.make_bytes(value)
        assert result == value
        assert isinstance(result, bytes)

    def test_make_bytes_with_str_input(self, response):
        value = 'test string'
        result = response.make_bytes(value)
        assert result == b'test string'
        assert isinstance(result, bytes)

    def test_make_bytes_with_non_string_input(self, response):
        value = 12345
        result = response.make_bytes(value)
        assert result == b'12345'
        assert isinstance(result, bytes)

    def test_make_bytes_with_empty_string(self, response):
        value = ''
        result = response.make_bytes(value)
        assert result == b''
        assert isinstance(result, bytes)

    def test_make_bytes_with_utf8_characters(self, response):
        value = 'Hello, 世界'
        result = response.make_bytes(value)
        assert result == b'Hello, \xe4\xb8\x96\xe7\x95\x8c'  # Expected result in bytes
        assert isinstance(result, bytes)