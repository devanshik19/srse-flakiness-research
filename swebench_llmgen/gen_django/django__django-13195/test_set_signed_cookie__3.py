import pytest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core import signing

class TestHttpResponseBase:
    
    def test_set_signed_cookie(self):
        # Create an instance of HttpResponse
        response = HttpResponse()

        # Test parameters
        key = 'test_key'
        value = 'test_value'
        salt = 'test_salt'

        # Call the set_signed_cookie method
        response.set_signed_cookie(key, value, salt=salt)

        # Check if the cookie is set correctly
        expected_value = signing.get_cookie_signer(salt=key + salt).sign(value)
        cookie_value = response.cookies[key].value
        
        assert cookie_value == expected_value
        assert response.cookies[key].secure is False  # By default, secure should be False
        assert response.cookies[key].httponly is False  # By default, httponly should be False

    def test_set_signed_cookie_with_kwargs(self):
        # Create an instance of HttpResponse
        response = HttpResponse()

        # Test parameters with additional kwargs
        key = 'test_key'
        value = 'test_value'
        salt = 'test_salt'
        max_age = 3600
        path = '/'

        # Call the set_signed_cookie method
        response.set_signed_cookie(key, value, salt=salt, max_age=max_age, path=path)

        # Check if the cookie is set correctly
        expected_value = signing.get_cookie_signer(salt=key + salt).sign(value)
        cookie_value = response.cookies[key].value
        
        assert cookie_value == expected_value
        assert response.cookies[key]['max-age'] == max_age
        assert response.cookies[key]['path'] == path