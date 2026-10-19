import pytest
from django.http import HttpResponseBase
from django.core import signing


class MockHttpResponse(HttpResponseBase):
    def set_cookie(self, key, value, **kwargs):
        # For testing purposes, we will just return the key and value as a tuple
        return key, value


def test_set_signed_cookie():
    response = MockHttpResponse('text/html', 200)
    
    # Prepare test data
    key = 'test_cookie'
    value = 'test_value'
    salt = 'some_salt'
    
    # Call the method under test
    signed_key, signed_value = response.set_signed_cookie(key, value, salt=salt)
    
    # Verify that the cookie value is signed
    expected_signed_value = signing.get_cookie_signer(salt=key + salt).sign(value)
    
    assert signed_key == key
    assert signed_value == expected_signed_value