import pytest
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.conf import settings

@pytest.fixture
def user_with_session(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def request_with_session(user_with_session):
    request = HttpRequest()
    request.session = {}
    request.session['BACKEND_SESSION_KEY'] = 'django.contrib.auth.backends.ModelBackend'
    request.session['HASH_SESSION_KEY'] = user_with_session.get_session_auth_hash()
    request.session['_auth_user_id'] = user_with_session.id
    return request

def test_get_user_with_existing_user(request_with_session, user_with_session):
    user = get_user(request_with_session)
    assert user == user_with_session

def test_get_user_with_anonymous_user():
    request = HttpRequest()
    request.session = {}
    user = get_user(request)
    assert user.is_anonymous

def test_get_user_with_invalid_backend(request_with_session):
    request_with_session.session['BACKEND_SESSION_KEY'] = 'invalid.backend'
    user = get_user(request_with_session)
    assert user.is_anonymous

def test_get_user_with_invalid_session_hash(request_with_session, user_with_session):
    request_with_session.session['HASH_SESSION_KEY'] = 'invalid_hash'
    user = get_user(request_with_session)
    assert user.is_anonymous