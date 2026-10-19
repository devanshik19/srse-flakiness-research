import pytest
from django.http import HttpResponseBase
from django.core import signing

class HttpResponseBaseTest(HttpResponseBase):
    def set_cookie(self, key, value, **kwargs):
        # Mock implementation of set_cookie just for testing
        self.cookie_set = {key: value, **kwargs}

def test_set_signed_cookie():
    response = HttpResponseBaseTest()
    key = 'test_key'
    value = 'test_value'
    salt = 'test_salt'
    
    # Call the set_signed_cookie method
    response.set_signed_cookie(key, value, salt=salt)
    
    # Check if the cookie is properly set and signed
    signer = signing.get_cookie_signer(salt=key + salt)
    signed_value = signer.sign(value)

    # Assert that the key exists in the cookies
    assert key in response.cookie_set
    # Assert that the value is the signed version of the original value
    assert response.cookie_set[key] == signed_value