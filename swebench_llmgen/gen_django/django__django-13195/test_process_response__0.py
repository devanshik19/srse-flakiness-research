import time
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponse
import pytest

def test_process_response_session_modified():
    middleware = SessionMiddleware(lambda request: HttpResponse())
    request = HttpRequest()
    user = User.objects.create_user(username='testuser', password='testpass')
    request.session = middleware.get_response(request)
    request.session['some_data'] = 'data'
    request.session.modified = True
    request.session.accessed = True
    response = middleware.process_response(request, HttpResponse())
    
    assert settings.SESSION_COOKIE_NAME in response.cookies
    assert response.cookies[settings.SESSION_COOKIE_NAME].value == request.session.session_key

def test_process_response_session_empty():
    middleware = SessionMiddleware(lambda request: HttpResponse())
    request = HttpRequest()
    request.session = middleware.get_response(request)
    request.session.clear()  # Making the session empty
    request.session.modified = True
    response = middleware.process_response(request, HttpResponse())
    
    assert settings.SESSION_COOKIE_NAME not in response.cookies

def test_process_response_no_modification():
    middleware = SessionMiddleware(lambda request: HttpResponse())
    request = HttpRequest()
    request.session = middleware.get_response(request)
    request.session.accessed = False
    request.session.modified = False
    response = middleware.process_response(request, HttpResponse())
    
    assert settings.SESSION_COOKIE_NAME not in response.cookies

def test_process_response_status_code_not_500():
    middleware = SessionMiddleware(lambda request: HttpResponse())
    request = HttpRequest()
    request.session = middleware.get_response(request)
    request.session['some_data'] = 'data'
    request.session.modified = True
    request.session.accessed = True
    response = middleware.process_response(request, HttpResponse(status=200))
    
    assert settings.SESSION_COOKIE_NAME in response.cookies

def test_process_response_status_code_500():
    middleware = SessionMiddleware(lambda request: HttpResponse())
    request = HttpRequest()
    request.session = middleware.get_response(request)
    request.session['some_data'] = 'data'
    request.session.modified = True
    request.session.accessed = True
    response = middleware.process_response(request, HttpResponse(status=500))
    
    assert settings.SESSION_COOKIE_NAME not in response.cookies