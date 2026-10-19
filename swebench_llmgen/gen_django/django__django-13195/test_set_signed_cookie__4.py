import pytest
from django.http import HttpResponseBase
from django.core import signing

class TestHttpResponseBase:
    
    @pytest.fixture
    def response(self):
        return HttpResponseBase(content_type='text/plain', status=200)

    def test_set_signed_cookie(self, response):
        key = 'my_cookie'
        value = 'cookie_value'
        salt = 'salt_value'
        
        # Sign the value manually to compare
        expected_signed_value = signing.get_cookie_signer(salt=key + salt).sign(value)

        # Set the signed cookie
        response.set_signed_cookie(key, value, salt=salt)

        # Retrieve the cookie to check if it's set correctly
        cookie_value = response.cookies.get(key).value
        
        assert cookie_value == expected_signed_value
        assert key in response.cookies
        assert response.cookies[key]['path'] == '/'
        
        # Check with additional kwargs
        response.set_signed_cookie(key, value, salt=salt, max_age=3600, httponly=True)
        assert response.cookies[key]['max-age'] == 3600
        assert response.cookies[key]['httponly'] is True