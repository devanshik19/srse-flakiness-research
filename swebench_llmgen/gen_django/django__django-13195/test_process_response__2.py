import time
import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.conf import settings

class MockSession:
    def __init__(self, accessed=False, modified=False, empty=False, session_key=None):
        self.accessed = accessed
        self.modified = modified
        self._empty = empty
        self.session_key = session_key

    def is_empty(self):
        return self._empty

    def save(self):
        if self.modified:
            self.session_key = 'test_session_key'

    def get_expiry_age(self):
        return 3600

    def get_expire_at_browser_close(self):
        return False


@pytest.mark.django_db
def test_process_response_delete_cookie():
    settings.SESSION_COOKIE_NAME = 'testid'
    settings.SESSION_COOKIE_PATH = '/'
    settings.SESSION_COOKIE_DOMAIN = None
    request = HttpRequest()
    request.COOKIES['testid'] = 'test_value'
    response = HttpResponse()
    request.session = MockSession(accessed=True, modified=False, empty=True)
    middleware = SessionMiddleware(lambda req: HttpResponse())

    response = middleware.process_response(request, response)

    assert 'testid' not in response.cookies


@pytest.mark.django_db
def test_process_response_set_cookie():
    settings.SESSION_COOKIE_NAME = 'testid'
    settings.SESSION_COOKIE_PATH = '/'
    settings.SESSION_COOKIE_DOMAIN = None
    request = HttpRequest()
    request.session = MockSession(accessed=True, modified=True, empty=False)
    response = HttpResponse()
    middleware = SessionMiddleware(lambda req: response)

    response = middleware.process_response(request, response)

    assert response.cookies['testid'].value == 'test_session_key'
    assert response.cookies['testid']['max-age'] == '3600'


@pytest.mark.django_db
def test_process_response_no_cookie_on_empty_session():
    settings.SESSION_COOKIE_NAME = 'testid'
    settings.SESSION_COOKIE_PATH = '/'
    settings.SESSION_COOKIE_DOMAIN = None
    request = HttpRequest()
    request.session = MockSession(accessed=True, modified=False, empty=False)
    response = HttpResponse()
    request.session.modified = True
    middleware = SessionMiddleware(lambda req: response)

    response = middleware.process_response(request, response)

    assert response.cookies['testid'].value == 'test_session_key'
    assert response.cookies['testid']['max-age'] == '3600'


@pytest.mark.django_db
def test_process_response_exception_on_update_error():
    settings.SESSION_COOKIE_NAME = 'testid'
    settings.SESSION_COOKIE_PATH = '/'
    settings.SESSION_COOKIE_DOMAIN = None

    class FailingSession:
        def save(self):
            raise UpdateError

    request = HttpRequest()
    request.session = FailingSession()
    response = HttpResponse()
    middleware = SessionMiddleware(lambda req: response)

    with pytest.raises(SuspiciousOperation):
        middleware.process_response(request, response)