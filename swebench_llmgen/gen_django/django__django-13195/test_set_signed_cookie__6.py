import pytest
from django.http import HttpResponse
from django.core import signing

class TestHttpResponseBase:
    def test_set_signed_cookie(self):
        response = HttpResponse()
        key = 'test_cookie'
        value = 'test_value'
        salt = 'test_salt'
        kwargs = {
            'max_age': 3600,
            'expires': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'path': '/',
            'domain': 'example.com',
            'secure': True,
            'httponly': True,
            'samesite': 'Lax'
        }

        # Setting the signed cookie
        response.set_signed_cookie(key, value, salt, **kwargs)

        # Retrieve cookie from the response
        cookie = response.cookies.get(key)

        # Assert cookie properties
        assert cookie is not None
        assert cookie.value == signing.get_cookie_signer(salt=key + salt).sign(value)
        assert cookie['max-age'] == '3600'
        assert cookie['expires'] is not None
        assert cookie['path'] == '/'
        assert cookie['domain'] == 'example.com'
        assert cookie['secure'] is True
        assert cookie['httponly'] is True
        assert cookie['samesite'] == 'Lax'