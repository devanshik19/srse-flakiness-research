import pytest
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.crypto import get_random_string

BACKEND_SESSION_KEY = 'django.contrib.auth.backends.ModelBackend'
HASH_SESSION_KEY = 'session_hash'

@pytest.fixture
def request_with_user(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    request = type('Request', (), {})()
    request.session = {}
    request.session[BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
    request.session['_auth_user_id'] = user.id
    request.session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    return request

@pytest.fixture
def request_without_user():
    request = type('Request', (), {})()
    request.session = {}
    return request

@pytest.fixture
def request_with_invalid_session_hash(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    request = type('Request', (), {})()
    request.session = {}
    request.session[BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
    request.session['_auth_user_id'] = user.id
    request.session[HASH_SESSION_KEY] = get_random_string()  # Invalid hash
    return request

def test_get_user_with_valid_session(request_with_user):
    user = get_user(request_with_user)
    assert user.is_authenticated
    assert user.username == 'testuser'

def test_get_user_with_no_user(request_without_user):
    user = get_user(request_without_user)
    assert not user.is_authenticated

def test_get_user_with_invalid_session_hash(request_with_invalid_session_hash):
    user = get_user(request_with_invalid_session_hash)
    assert not user.is_authenticated