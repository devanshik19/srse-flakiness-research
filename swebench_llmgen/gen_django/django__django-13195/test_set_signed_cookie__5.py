import pytest
from django.http import HttpResponseBase
from django.contrib.auth.models import User
from django.core import signing

class TestHttpResponseBase:

    def test_set_signed_cookie(self):
        response = HttpResponseBase('text/html')
        key = 'user_id'
        value = '12345'
        salt = 'my_salt'
        
        # Expected signed value
        signer = signing.get_cookie_signer(salt=key + salt)
        expected_signed_value = signer.sign(value)
        
        response.set_signed_cookie(key, value, salt=salt)

        # Check if the cookie is set correctly
        cookie_value = response.cookies[key].value
        assert cookie_value == expected_signed_value
        assert response.cookies[key]['max-age'] is None
        assert response.cookies[key]['path'] is None
        assert response.cookies[key]['domain'] is None
        assert response.cookies[key]['secure'] is None
        assert response.cookies[key]['httponly'] is None
        assert response.cookies[key]['samesite'] is None

    def test_set_signed_cookie_with_kwargs(self):
        response = HttpResponseBase('text/html')
        key = 'session_id'
        value = 'abcde'
        salt = 'session_salt'

        # Expected signed value
        signer = signing.get_cookie_signer(salt=key + salt)
        expected_signed_value = signer.sign(value)

        # Set additional cookie parameters
        response.set_signed_cookie(key, value, salt=salt, max_age=3600, path='/', secure=True, httponly=True, samesite='Lax')

        # Check if the cookie is set with additional parameters
        cookie_value = response.cookies[key].value
        assert cookie_value == expected_signed_value
        assert response.cookies[key]['max-age'] == '3600'
        assert response.cookies[key]['path'] == '/'
        assert response.cookies[key]['secure'] == 'True'
        assert response.cookies[key]['httponly'] == 'True'
        assert response.cookies[key]['samesite'] == 'Lax'