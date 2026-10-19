import pytest
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY

class TestGetUser:
    def test_get_user_authenticated(self, client):
        user = User.objects.create_user(username='testuser', password='testpass')
        backend = ModelBackend()
        backend.get_user(user.id)  # Authenticate user with the backend

        # Simulate a request session with valid data
        client.login(username='testuser', password='testpass')
        session = client.session
        session[SESSION_KEY] = user.id
        session[BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()

        request = client.get('/').wsgi_request
        retrieved_user = get_user(request)

        assert retrieved_user.id == user.id

    def test_get_user_anonymous(self, client):
        request = client.get('/').wsgi_request
        retrieved_user = get_user(request)

        assert isinstance(retrieved_user, User) and not retrieved_user.is_authenticated

    def test_get_user_invalid_backend(self, client):
        user = User.objects.create_user(username='testuser', password='testpass')

        # Simulate a request session with a non-existent backend
        client.login(username='testuser', password='testpass')
        session = client.session
        session[SESSION_KEY] = user.id
        session[BACKEND_SESSION_KEY] = 'invalid.backend'
        session.save()

        request = client.get('/').wsgi_request
        retrieved_user = get_user(request)

        assert isinstance(retrieved_user, User) and not retrieved_user.is_authenticated

    def test_get_user_session_hash_mismatch(self, client):
        user = User.objects.create_user(username='testuser', password='testpass')

        # Simulate a request session with a valid backend and user
        client.login(username='testuser', password='testpass')
        session = client.session
        session[SESSION_KEY] = user.id
        session[BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
        session[HASH_SESSION_KEY] = 'invalid_hash'
        session.save()

        request = client.get('/').wsgi_request
        retrieved_user = get_user(request)

        assert isinstance(retrieved_user, User) and not retrieved_user.is_authenticated