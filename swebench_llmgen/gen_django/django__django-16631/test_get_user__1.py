import pytest
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

@pytest.fixture
def user_settings(settings):
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def request_with_user(create_user):
    request = HttpRequest()
    request.session = {
        'user_id': create_user.id,
        'backend': 'django.contrib.auth.backends.ModelBackend',
        'hash_session_key': create_user.get_session_auth_hash(),
    }
    return request

@pytest.fixture
def request_without_user():
    request = HttpRequest()
    request.session = {}
    return request

def test_get_user_with_valid_session(user_settings, request_with_user, create_user):
    user = get_user(request_with_user)
    assert user.id == create_user.id
    assert user.username == 'testuser'

def test_get_user_with_invalid_session(user_settings, request_with_user, create_user):
    request_with_user.session['hash_session_key'] = 'invalid_hash'
    user = get_user(request_with_user)
    assert isinstance(user, AnonymousUser)

def test_get_user_with_missing_backend(user_settings, request_without_user):
    user = get_user(request_without_user)
    assert isinstance(user, AnonymousUser)

def test_get_user_with_nonexistent_user(user_settings, request_without_user):
    request_without_user.session = {
        'user_id': 9999,  # Non-existent user ID
        'backend': 'django.contrib.auth.backends.ModelBackend',
    }
    user = get_user(request_without_user)
    assert isinstance(user, AnonymousUser)