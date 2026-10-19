import pytest
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class CustomBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

@pytest.fixture
def user(client):
    user = User.objects.create_user(username='testuser', password='password')
    return user

def test_get_user_with_valid_session(client, user):
    client.login(username='testuser', password='password')
    request = client

    # Simulate creating a user session in the request
    request.session['_auth_user_id'] = user.id
    request.session['BACKEND_SESSION_KEY'] = 'django.contrib.auth.backends.ModelBackend'
    settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
    
    retrieved_user = get_user(request)
    
    assert retrieved_user.id == user.id
    assert retrieved_user.username == 'testuser'

def test_get_user_with_invalid_session_key(client):
    request = client

    # No user logged in
    request.session = {}
    
    retrieved_user = get_user(request)
    
    assert isinstance(retrieved_user, AnonymousUser)

def test_get_user_with_invalid_backend(client, user):
    client.login(username='testuser', password='password')
    request = client

    # Simulate creating a user session in the request with an invalid backend
    request.session['_auth_user_id'] = user.id
    request.session['BACKEND_SESSION_KEY'] = 'invalid.backend.Path'
    settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
    
    with pytest.raises(ImproperlyConfigured):
        get_user(request)