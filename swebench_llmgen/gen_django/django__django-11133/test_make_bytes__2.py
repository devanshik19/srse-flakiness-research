import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:
    @pytest.fixture
    def response(self):
        return HttpResponseBase(content_type='text/html', status=200, reason='OK', charset='utf-8')

    def test_make_bytes_with_bytes(self, response):
        value = b'This is a byte string'
        result = response.make_bytes(value)
        assert result == value

    def test_make_bytes_with_string(self, response):
        value = 'This is a string'
        result = response.make_bytes(value)
        assert result == b'This is a string'
    
    def test_make_bytes_with_int(self, response):
        value = 123
        result = response.make_bytes(value)
        assert result == b'123'
    
    def test_make_bytes_with_float(self, response):
        value = 123.456
        result = response.make_bytes(value)
        assert result == b'123.456'
    
    def test_make_bytes_with_list(self, response):
        value = ['item1', 'item2']
        result = response.make_bytes(value)
        assert result == b"['item1', 'item2']"
    
    def test_make_bytes_with_dict(self, response):
        value = {'key': 'value'}
        result = response.make_bytes(value)
        assert result == b"{'key': 'value'}"