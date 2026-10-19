import json
from django.conf import settings
from django.contrib.messages.storage.cookie import CookieStorage
from django.contrib.auth.models import User
from django.http import HttpResponse

def test_update_cookie_sets_cookie_when_encoded_data_provided():
    # Arrange
    storage = CookieStorage()
    response = HttpResponse()
    encoded_data = json.dumps({"messages": ["Test message"]})
    
    # Act
    storage._update_cookie(encoded_data, response)
    
    # Assert
    assert response.cookies[storage.cookie_name].value == encoded_data
    assert response.cookies[storage.cookie_name]['domain'] == settings.SESSION_COOKIE_DOMAIN
    assert response.cookies[storage.cookie_name]['secure'] == (settings.SESSION_COOKIE_SECURE or None)
    assert response.cookies[storage.cookie_name]['httponly'] == (settings.SESSION_COOKIE_HTTPONLY or None)
    assert response.cookies[storage.cookie_name]['samesite'] == settings.SESSION_COOKIE_SAMESITE

def test_update_cookie_deletes_cookie_when_no_encoded_data():
    # Arrange
    storage = CookieStorage()
    response = HttpResponse()
    storage.cookie_name = 'test_cookie'
    
    # Act
    storage._update_cookie(None, response)
    
    # Assert
    assert storage.cookie_name not in response.cookies