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

def test_update_cookie_with_data(cookie_storage, response):
    encoded_data = json.dumps({'messages': ['Hello, World!']})
    cookie_storage.cookie_name = 'test_cookie'
    
    cookie_storage._update_cookie(encoded_data, response)
    
    assert response.cookies[cookie_storage.cookie_name].value == encoded_data
    assert response.cookies[cookie_storage.cookie_name].domain == settings.SESSION_COOKIE_DOMAIN

def test_update_cookie_without_data(cookie_storage, response):
    cookie_storage.cookie_name = 'test_cookie'
    
    cookie_storage._update_cookie('', response)
    
    assert cookie_storage.cookie_name not in response.cookies

def test_update_cookie_secure_flag(cookie_storage, response):
    cookie_storage.cookie_name = 'test_cookie'
    encoded_data = json.dumps({'messages': ['Secure Test']})
    settings.SESSION_COOKIE_SECURE = True
    
    cookie_storage._update_cookie(encoded_data, response)
    
    assert response.cookies[cookie_storage.cookie_name]['secure'] is True

def test_update_cookie_http_only_flag(cookie_storage, response):
    cookie_storage.cookie_name = 'test_cookie'
    encoded_data = json.dumps({'messages': ['HttpOnly Test']})
    settings.SESSION_COOKIE_HTTPONLY = True
    
    cookie_storage._update_cookie(encoded_data, response)
    
    assert response.cookies[cookie_storage.cookie_name]['httponly'] is True

def test_update_cookie_same_site_flag(cookie_storage, response):
    cookie_storage.cookie_name = 'test_cookie'
    encoded_data = json.dumps({'messages': ['SameSite Test']})
    settings.SESSION_COOKIE_SAMESITE = 'Lax'
    
    cookie_storage._update_cookie(encoded_data, response)
    
    assert response.cookies[cookie_storage.cookie_name]['samesite'] == 'Lax'