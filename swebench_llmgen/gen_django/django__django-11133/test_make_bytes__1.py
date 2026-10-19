import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:
    
    @pytest.fixture
    def response(self):
        return HttpResponseBase('text/plain', status=200, reason='OK', charset='utf-8')

    def test_make_bytes_with_bytes_input(self, response):
        result = response.make_bytes(b'This is already bytes.')
        assert result == b'This is already bytes.'
        assert isinstance(result, bytes)

    def test_make_bytes_with_str_input(self, response):
        result = response.make_bytes('This is a string.')
        assert result == b'This is a string.'
        assert isinstance(result, bytes)

    def test_make_bytes_with_non_string_input(self, response):
        result = response.make_bytes(12345)
        assert result == b'12345'
        assert isinstance(result, bytes)

    def test_make_bytes_with_empty_string(self, response):
        result = response.make_bytes('')
        assert result == b''
        assert isinstance(result, bytes)

    def test_make_bytes_with_complex_object(self, response):
        result = response.make_bytes({'key': 'value'})
        assert result == b"{'key': 'value'}"
        assert isinstance(result, bytes)

    def test_make_bytes_with_custom_charset(self):
        response = HttpResponseBase('text/plain', status=200, reason='OK', charset='latin1')
        result = response.make_bytes('This is a string.')
        assert result == b'This is a string.'.decode('utf-8').encode('latin1')
        assert isinstance(result, bytes)