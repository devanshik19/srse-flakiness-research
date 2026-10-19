import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:

    @pytest.fixture
    def http_response(self):
        return HttpResponseBase(content_type='text/plain', status=200, reason='OK', charset='utf-8')

    def test_make_bytes_with_bytes_input(self, http_response):
        input_value = b'Test bytes'
        result = http_response.make_bytes(input_value)
        assert result == input_value
        assert isinstance(result, bytes)

    def test_make_bytes_with_string_input(self, http_response):
        input_value = 'Test string'
        result = http_response.make_bytes(input_value)
        assert result == b'Test string'
        assert isinstance(result, bytes)

    def test_make_bytes_with_non_string_input(self, http_response):
        input_value = 12345
        result = http_response.make_bytes(input_value)
        assert result == b'12345'
        assert isinstance(result, bytes)

    def test_make_bytes_with_empty_string(self, http_response):
        input_value = ''
        result = http_response.make_bytes(input_value)
        assert result == b''
        assert isinstance(result, bytes)

    def test_make_bytes_with_none_input(self, http_response):
        input_value = None
        result = http_response.make_bytes(input_value)
        assert result == b'None'
        assert isinstance(result, bytes)