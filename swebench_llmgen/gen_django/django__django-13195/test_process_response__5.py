import time
import pytest
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.utils.http import http_date


@pytest.fixture
def session_middleware():
    return SessionMiddleware(lambda request: HttpResponse())


@pytest.fixture
def user_with_session():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user


def test_process_response_with_modified_session(session_middleware, user_with_session):
    request = HttpRequest()
    request.session = user_with_session.create_linked_session()
    request.session.modified = True
    response = HttpResponse()

    response = session_middleware.process_response(request, response)

    assert response.cookies[settings.SESSION_COOKIE_NAME].value == request.session.session_key


def test_process_response_with_empty_session(session_middleware, user_with_session):
    request = HttpRequest()
    request.session = user_with_session.create_linked_session()
    request.session.clear()  # Make the session empty
    response = HttpResponse()
    request.COOKIES[settings.SESSION_COOKIE_NAME] = request.session.session_key

    response = session_middleware.process_response(request, response)

    assert settings.SESSION_COOKIE_NAME not in response.cookies  # Cookie should be deleted


def test_process_response_with_accessed_session(session_middleware, user_with_session):
    request = HttpRequest()
    request.session = user_with_session.create_linked_session()
    request.session.accessed = True
    response = HttpResponse()

    response = session_middleware.process_response(request, response)

    assert 'Cookie' in response.vary  # Cookie should be varied


def test_process_response_without_session(session_middleware):
    request = HttpRequest()
    response = HttpResponse()

    response = session_middleware.process_response(request, response)

    assert response.status_code == 200  # Should return response without error