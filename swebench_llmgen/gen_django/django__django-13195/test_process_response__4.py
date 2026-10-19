import pytest
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpRequest, HttpResponse
from django.conf import settings

@pytest.fixture
def session_middleware():
    return SessionMiddleware(lambda request: HttpResponse())

@pytest.fixture
def user_with_session(client):
    user = User.objects.create_user('testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    return user

def test_process_response_session_modified(session_middleware, user_with_session):
    request = HttpRequest()
    request.session = SessionStore()
    request.session['key'] = 'value'
    request.session.modified = True
    request.session.accessed = True
    request.session.save()
    response = HttpResponse()

    response = session_middleware.process_response(request, response)

    assert response.cookies[settings.SESSION_COOKIE_NAME]['value'] == request.session.session_key

def test_process_response_session_empty(session_middleware, user_with_session):
    request = HttpRequest()
    request.session = SessionStore()
    request.session.clear_expired()
    request.session.modified = False
    request.session.accessed = True
    request.session.save()
    request.COOKIES[settings.SESSION_COOKIE_NAME] = request.session.session_key
    response = HttpResponse()

    response = session_middleware.process_response(request, response)

    assert settings.SESSION_COOKIE_NAME not in response.cookies

def test_process_response_http_error(session_middleware, user_with_session):
    request = HttpRequest()
    request.session = SessionStore()
    request.session['key'] = 'value'
    request.session.modified = True
    request.session.accessed = True
    request.session.save()
    response = HttpResponse(status=500)

    response = session_middleware.process_response(request, response)

    assert settings.SESSION_COOKIE_NAME not in response.cookies

def test_process_response_no_attribute_error(session_middleware):
    request = HttpRequest()
    response = HttpResponse()

    response = session_middleware.process_response(request, response)

    assert response == response  # Check if response is unchanged when no session