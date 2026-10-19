import json
from django.conf import settings
from django.contrib.messages.storage.cookie import CookieStorage
from django.http import HttpResponse
import pytest

@pytest.fixture
def cookie_storage():
    return CookieStorage()

@pytest.fixture
def response():
    return HttpResponse()

def test_update_cookie_sets_cookie(cookie_storage, response):
    encoded_data = json.dumps({"messages": ["Test message"]})
    cookie_storage.cookie_name = 'test_cookie'
    
    cookie_storage._update_cookie(encoded_data, response)
    
    assert response.cookies[cookie_storage.cookie_name].value == encoded_data
    assert response.cookies[cookie_storage.cookie_name].path == '/'
    assert response.cookies[cookie_storage.cookie_name]['domain'] == settings.SESSION_COOKIE_DOMAIN
    assert response.cookies[cookie_storage.cookie_name]['secure'] == (settings.SESSION_COOKIE_SECURE or None)
    assert response.cookies[cookie_storage.cookie_name]['httponly'] == (settings.SESSION_COOKIE_HTTPONLY or None)
    assert response.cookies[cookie_storage.cookie_name]['samesite'] == settings.SESSION_COOKIE_SAMESITE

def test_update_cookie_deletes_cookie(cookie_storage, response):
    cookie_storage.cookie_name = 'test_cookie'
    
    cookie_storage._update_cookie(None, response)
    
    assert cookie_storage.cookie_name not in response.cookies