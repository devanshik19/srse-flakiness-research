import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:

    @pytest.fixture
    def response(self):
        return HttpResponseBase('text/html', status=200, reason=None, charset='utf-8')

    def test_make_bytes_with_bytes(self, response):
        value = b'This is a byte string'
        result = response.make_bytes(value)
        assert result == value

    def test_make_bytes_with_str(self, response):
        value = 'This is a string'
        result = response.make_bytes(value)
        assert result == b'This is a string'

    def test_make_bytes_with_non_string(self, response):
        value = 1234
        result = response.make_bytes(value)
        assert result == b'1234'

    def test_make_bytes_with_none(self, response):
        value = None
        result = response.make_bytes(value)
        assert result == b'None'