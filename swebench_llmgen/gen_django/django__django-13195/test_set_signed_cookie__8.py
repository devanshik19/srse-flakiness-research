import pytest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core import signing

class TestHttpResponseBase:

    def test_set_signed_cookie(self):
        response = HttpResponse()
        key = 'test_key'
        value = 'test_value'
        salt = 'test_salt'
        kwargs = {
            'max_age': 3600,
            'expires': None,
            'path': '/',
            'domain': None,
            'secure': False,
            'httponly': False,
            'samesite': None
        }

        # Set the signed cookie
        cookie = response.set_signed_cookie(key, value, salt, **kwargs)

        # Check if cookie is set properly
        assert key in response.cookies
        assert response.cookies[key].value == signing.get_cookie_signer(salt=key + salt).sign(value)
        assert response.cookies[key]['max-age'] == 3600
        assert response.cookies[key]['path'] == '/'
        assert response.cookies[key]['secure'] is False
        assert response.cookies[key]['httponly'] is False
        assert response.cookies[key]['samesite'] is None

    def test_set_signed_cookie_with_different_salt(self):
        response = HttpResponse()
        key = 'test_key'
        value = 'test_value'
        salt = 'different_salt'
        kwargs = {}

        # Set the signed cookie with different salt
        cookie = response.set_signed_cookie(key, value, salt, **kwargs)

        # Check if cookie is set with different signature
        assert key in response.cookies
        assert response.cookies[key].value == signing.get_cookie_signer(salt=key + salt).sign(value)

    def test_set_signed_cookie_without_optional_args(self):
        response = HttpResponse()
        key = 'test_key'
        value = 'test_value'

        # Set the signed cookie without any optional arguments
        response.set_signed_cookie(key, value)

        # Check if cookie is set properly
        assert key in response.cookies
        assert response.cookies[key].value == signing.get_cookie_signer(salt=key).sign(value)
        assert response.cookies[key]['max-age'] is None
        assert response.cookies[key]['path'] == '/'
        assert response.cookies[key]['secure'] is False
        assert response.cookies[key]['httponly'] is False
        assert response.cookies[key]['samesite'] is None