import json
from django.conf import settings
from django.contrib.messages.storage.cookie import CookieStorage
from django.http import HttpResponse
import pytest

@pytest.mark.django_db
def test_update_cookie_set():
    storage = CookieStorage()
    storage.cookie_name = 'test_cookie'
    response = HttpResponse()

    encoded_data = json.dumps({'messages': ['Test message']})
    storage._update_cookie(encoded_data, response)

    assert response.cookies['test_cookie'].value == encoded_data
    assert response.cookies['test_cookie']['domain'] == settings.SESSION_COOKIE_DOMAIN
    assert response.cookies['test_cookie']['secure'] == (settings.SESSION_COOKIE_SECURE or None)
    assert response.cookies['test_cookie']['httponly'] == (settings.SESSION_COOKIE_HTTPONLY or None)
    assert response.cookies['test_cookie']['samesite'] == settings.SESSION_COOKIE_SAMESITE

def test_update_cookie_delete():
    storage = CookieStorage()
    storage.cookie_name = 'test_cookie'
    response = HttpResponse()

    storage._update_cookie(None, response)

    assert 'test_cookie' not in response.cookies