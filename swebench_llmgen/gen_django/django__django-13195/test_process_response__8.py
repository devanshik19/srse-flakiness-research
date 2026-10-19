import time
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.http import HttpResponse

def test_process_response():
    # Setting up the request factory and middleware
    factory = RequestFactory()
    middleware = SessionMiddleware(lambda request: HttpResponse(""))

    user = User.objects.create_user(username='testuser', password='testpass')
    request = factory.get('/')
    request.user = user

    # Create a session
    request.session = SessionStore()
    request.session['key'] = 'value'
    request.session.modified = True
    request.session.accessed = True

    # Test saving session data
    response = middleware.process_response(request, HttpResponse())
    assert response.cookies[settings.SESSION_COOKIE_NAME]['value'] == request.session.session_key

    # Test that cookie is set when session is modified
    request.session.modified = False
    response = middleware.process_response(request, HttpResponse())
    assert settings.SESSION_COOKIE_NAME in response.cookies

    # Test deleting cookie when session is empty
    request.session.clear()
    request.session.accessed = True
    response = middleware.process_response(request, response)
    assert settings.SESSION_COOKIE_NAME not in response.cookies

    # Raise SuspiciousOperation on UpdateError
    request.session = SessionStore()
    request.session.modified = True
    request.session.accessed = True
    request.session.save = lambda: (_ for _ in ()).throw(UpdateError('Simulated error'))
    
    with pytest.raises(SuspiciousOperation):
        middleware.process_response(request, HttpResponse())