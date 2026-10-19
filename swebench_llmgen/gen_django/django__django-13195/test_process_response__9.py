import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.conf import settings

@pytest.fixture
def session_middleware():
    return SessionMiddleware(lambda request: HttpResponse())

@pytest.fixture
def client_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def request_with_session(client_user):
    request = HttpRequest()
    request.session = SessionStore()
    request.session.create()
    request.session['_auth_user_id'] = str(client_user.id)
    request.user = client_user
    return request

def test_process_response_saves_session(session_middleware, request_with_session):
    request_with_session.session.modified = True
    request_with_session.session.accessed = True
    response = HttpResponse()
    
    updated_response = session_middleware.process_response(request_with_session, response)
    
    assert updated_response == response
    assert request_with_session.session.session_key in updated_response.cookies
    assert updated_response.cookies[settings.SESSION_COOKIE_NAME]['max-age'] is not None

def test_process_response_deletes_cookie_on_empty_session(session_middleware):
    request = HttpRequest()
    request.session = SessionStore()
    request.session.create()
    request.session.clear_expired()

    response = HttpResponse()
    request.COOKIES[settings.SESSION_COOKIE_NAME] = 'session_id'
    request.session.accessed = True
    request.session.modified = False

    updated_response = session_middleware.process_response(request, response)

    assert 'session_id' not in updated_response.cookies

def test_process_response_does_not_save_on_500_response(session_middleware, request_with_session):
    request_with_session.session.modified = True
    request_with_session.session.accessed = True
    response = HttpResponse(status=500)

    updated_response = session_middleware.process_response(request_with_session, response)

    assert updated_response == response
    assert request_with_session.session.session_key not in updated_response.cookies

def test_process_response_raises_exception_on_update_error(session_middleware, request_with_session):
    request_with_session.session.modified = True
    request_with_session.session.accessed = True

    def raise_update_error():
        raise UpdateError("Test error")

    request_with_session.session.save = raise_update_error

    with pytest.raises(SuspiciousOperation):
        session_middleware.process_response(request_with_session, HttpResponse())