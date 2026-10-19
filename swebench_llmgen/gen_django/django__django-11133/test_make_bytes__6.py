import pytest
from django.http.response import HttpResponseBase

class TestHttpResponseBase:

    @pytest.fixture
    def response(self):
        return HttpResponseBase(content_type='text/plain', status=200, reason='OK', charset='utf-8')

    def test_make_bytes_with_bytes(self, response):
        value = b'test bytes'
        assert response.make_bytes(value) == value

    def test_make_bytes_with_str(self, response):
        value = 'test string'
        expected = b'test string'
        assert response.make_bytes(value) == expected

    def test_make_bytes_with_non_string(self, response):
        value = 12345
        expected = b'12345'
        assert response.make_bytes(value) == expected

    def test_make_bytes_with_unicode_string(self, response):
        value = 'üñîçødë'
        expected = b'üñîçødë'
        assert response.make_bytes(value) == expected

    def test_make_bytes_with_different_charset(self):
        response = HttpResponseBase(content_type='text/plain', status=200, reason='OK', charset='latin-1')
        value = 'test string'
        expected = b'test string'
        assert response.make_bytes(value) == expected