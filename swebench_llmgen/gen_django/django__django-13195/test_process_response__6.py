import time
import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.http import http_date
from django.contrib.sessions.middleware import SessionMiddleware

@pytest.fixture
def session_middleware():
    return SessionMiddleware(lambda request: HttpResponse())

@pytest.fixture
def user_with_session(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    return user

def test_process_response_session_modified(session_middleware, user_with_session, settings):
    settings.SESSION_SAVE_EVERY_REQUEST = False
    settings.SESSION_COOKIE_NAME = 'sessionid'
    settings.SESSION_COOKIE_PATH = '/'
    settings.SESSION_COOKIE_SECURE = False
    settings.SESSION_COOKIE_HTTPONLY = True
    settings.SESSION_COOKIE_SAMESITE = 'Lax'
    
    request = user_with_session
    request.session.modified = True
    request.session.session_key = 'testkey'
    request.session.accessed = True
    request.session.is_empty = lambda: False
    request.session.get_expiry_age = lambda: 300
    request.session.get_expire_at_browser_close = lambda: False
    response = HttpResponse()

    response = session_middleware.process_response(request, response)

    assert response.cookies[settings.SESSION_COOKIE_NAME]['value'] == 'testkey'
    assert response.cookies[settings.SESSION_COOKIE_NAME]['max_age'] == 300

def test_process_response_session_empty(session_middleware, user_with_session, settings):
    settings.SESSION_COOKIE_NAME = 'sessionid'
    settings.SESSION_COOKIE_PATH = '/'
    
    request = user_with_session
    request.session.modified = False
    request.session.session_key = 'testkey'
    request.session.accessed = True
    request.session.is_empty = lambda: True
    response = HttpResponse()

    response = session_middleware.process_response(request, response)

    assert response.cookies.get(settings.SESSION_COOKIE_NAME) is None

def test_process_response_session_update_error(session_middleware, user_with_session, settings):
    settings.SESSION_COOKIE_NAME = 'sessionid'
    
    request = user_with_session
    request.session.modified = True
    request.session.session_key = 'testkey'
    request.session.accessed = True
    request.session.is_empty = lambda: False
    request.session.save = lambda: (_ for _ in ()).throw(UpdateError("Demo error"))  # Simulate an UpdateError
    response = HttpResponse()

    with pytest.raises(SuspiciousOperation) as excinfo:
        session_middleware.process_response(request, response)

    assert "The request's session was deleted before the request completed." in str(excinfo.value)

def test_process_response_no_cookie_name(session_middleware, user_with_session, settings):
    request = user_with_session
    request.session = None  # Simulate no session
    response = HttpResponse()

    response = session_middleware.process_response(request, response)
    
    assert response == response  # Just checking the response returns unchanged