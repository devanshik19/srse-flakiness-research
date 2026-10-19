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

def test_update_cookie_sets_cookie_when_encoded_data_present(cookie_storage, response):
    encoded_data = json.dumps({'some': 'data'})
    cookie_storage.cookie_name = 'test_cookie'
    
    cookie_storage._update_cookie(encoded_data, response)

    assert 'test_cookie' in response.cookies
    assert response.cookies['test_cookie'].value == encoded_data

def test_update_cookie_deletes_cookie_when_no_encoded_data(cookie_storage, response):
    cookie_storage.cookie_name = 'test_cookie'
    
    # Simulate setting a cookie first
    response.set_cookie('test_cookie', 'some_value')
    
    cookie_storage._update_cookie(None, response)

    assert 'test_cookie' not in response.cookies