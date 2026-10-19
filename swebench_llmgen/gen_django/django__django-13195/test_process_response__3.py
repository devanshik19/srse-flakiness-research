import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.conf import settings

@pytest.fixture
def session_middleware():
    return SessionMiddleware(lambda req: HttpResponse())

@pytest.fixture
def setup_user_session():
    user = User.objects.create_user(username='testuser', password='testpassword')
    request = HttpRequest()
    request.session = {}
    request.user = user
    return request

def test_process_response_session_modified(session_middleware, setup_user_session):
    request = setup_user_session
    request.session['key'] = 'value'
    request.session.modified = True
    response = HttpResponse()
    
    response = session_middleware.process_response(request, response)
    
    assert response.cookies[settings.SESSION_COOKIE_NAME].value == request.session.session_key
    assert response.cookies[settings.SESSION_COOKIE_NAME]['httponly'] == ('True' if settings.SESSION_COOKIE_HTTPONLY else None)

def test_process_response_session_empty(session_middleware, setup_user_session):
    request = setup_user_session
    request.session.clear()
    request.session.modified = False
    response = HttpResponse()
    request.COOKIES[settings.SESSION_COOKIE_NAME] = 'dummy_session_key'
    
    response = session_middleware.process_response(request, response)
    
    assert settings.SESSION_COOKIE_NAME not in response.cookies

def test_process_response_session_not_modified(session_middleware, setup_user_session):
    request = setup_user_session
    request.session['key'] = 'value'
    request.session.accessed = True
    request.session.modified = False
    response = HttpResponse()
    
    response = session_middleware.process_response(request, response)
    
    assert response.cookies[settings.SESSION_COOKIE_NAME].value == request.session.session_key

def test_process_response_http_error_status_code(session_middleware, setup_user_session):
    request = setup_user_session
    request.session['key'] = 'value'
    request.session.modified = True
    response = HttpResponse(status=500)
    
    response = session_middleware.process_response(request, response)
    
    assert settings.SESSION_COOKIE_NAME not in response.cookies