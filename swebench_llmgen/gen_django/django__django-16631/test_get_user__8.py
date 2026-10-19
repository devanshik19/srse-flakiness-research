import pytest
from django.contrib.auth.models import User
from django.contrib.auth import get_user as get_user_function
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.conf import settings

BACKEND_SESSION_KEY = 'backend'
HASH_SESSION_KEY = 'hash'

@pytest.fixture
def request_with_user(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    request = HttpRequest()
    request.session = {}
    request.session[BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
    request.session['_auth_user_id'] = str(user.id)
    request.session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    return request

@pytest.fixture
def request_without_user():
    request = HttpRequest()
    request.session = {}
    return request

def test_get_user_valid_user(request_with_user):
    user = get_user_function(request_with_user)
    assert user.is_authenticated
    assert user.username == 'testuser'

def test_get_user_anonymous_user(request_without_user):
    user = get_user_function(request_without_user)
    assert not user.is_authenticated
    assert user.username == 'AnonymousUser'

def test_get_user_invalid_hash(request_with_user):
    request_with_user.session[HASH_SESSION_KEY] = 'wrong_hash'
    user = get_user_function(request_with_user)
    assert not user.is_authenticated
    assert user.username == 'AnonymousUser'

def test_get_user_no_backend_key(request_without_user):
    user = get_user_function(request_without_user)
    assert not user.is_authenticated
    assert user.username == 'AnonymousUser'