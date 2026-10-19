import pytest
from django.contrib.messages.storage.cookie import CookieStorage
from django.http import HttpResponse

@pytest.fixture
def cookie_storage():
    return CookieStorage()

def test_update_cookie_sets_cookie_with_data(cookie_storage):
    response = HttpResponse()
    encoded_data = json.dumps({'messages': ['Test message']})
    cookie_storage.cookie_name = 'test_cookie'

    cookie_storage._update_cookie(encoded_data, response)

    assert response.cookies[cookie_storage.cookie_name].value == encoded_data
    assert response.cookies[cookie_storage.cookie_name]['domain'] == None  # Assuming domain is None

def test_update_cookie_deletes_cookie_without_data(cookie_storage):
    response = HttpResponse()
    cookie_storage.cookie_name = 'test_cookie'

    cookie_storage._update_cookie(None, response)

    assert cookie_storage.cookie_name not in response.cookies