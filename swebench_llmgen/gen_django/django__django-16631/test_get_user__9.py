import pytest
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.crypto import get_random_string

@pytest.fixture
def request_with_user(client):
    # Create a user and log them in
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    # Create a request and add session middleware
    request = client.get('/')
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.flush()  # To ensure a clean session
    # Manually set the required session keys
    request.session['_auth_user_id'] = user.id
    request.session['backend'] = 'django.contrib.auth.backends.ModelBackend'
    
    return request

@pytest.fixture
def request_anonymous(client):
    # Create a request without a user logged in
    request = client.get('/')
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.flush()  # Ensure no session data is present
    return request

def test_get_user_with_authenticated_user(request_with_user):
    user = get_user(request_with_user)
    assert user.is_authenticated
    assert user.username == 'testuser'

def test_get_user_without_authenticated_user(request_anonymous):
    user = get_user(request_anonymous)
    assert not user.is_authenticated
    assert user.username == 'AnonymousUser'