import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings

class MockRequest:
    def __init__(self, session):
        self.session = session
        self.COOKIES = {}

class MockSession:
    def __init__(self, accessed=False, modified=False, empty=False):
        self.accessed = accessed
        self.modified = modified
        self._empty = empty
        self.session_key = "mock_session_key"

    def is_empty(self):
        return self._empty

    def save(self):
        if self.modified:
            self.modified = False  # simulate saving behavior

    def get_expiry_age(self):
        return 3600  # simulate 1 hour expiry

    def get_expire_at_browser_close(self):
        return False  # simulate the cookie not expiring at browser close

@pytest.mark.parametrize("accessed, modified, empty, expected_status_code", [
    (False, False, True, 200),  # session empty, no cookie set
    (True, False, False, 200),   # accessed, not modified
    (True, True, False, 200),    # accessed and modified
])
def test_process_response(accessed, modified, empty, expected_status_code):
    settings.SESSION_COOKIE_NAME = 'sessionid'
    settings.SESSION_COOKIE_PATH = '/'
    settings.SESSION_COOKIE_DOMAIN = None
    settings.SESSION_COOKIE_SECURE = False
    settings.SESSION_COOKIE_HTTPONLY = False
    settings.SESSION_COOKIE_SAMESITE = 'Lax'

    session = MockSession(accessed=accessed, modified=modified, empty=empty)
    request = MockRequest(session)
    response = HttpResponse()

    middleware = SessionMiddleware(lambda req: response)
    response = middleware.process_response(request, response)

    if empty:
        assert 'sessionid' not in response.cookies  # session should be deleted
    else:
        assert response.cookies['sessionid'].value == session.session_key  # session should be set
    assert response.status_code == expected_status_code

def test_process_response_raises_suspicious_operation_on_update_error():
    class UpdateErrorSession(MockSession):
        def save(self):
            raise UpdateError()

    session = UpdateErrorSession(modified=True)
    request = MockRequest(session)
    response = HttpResponse()

    middleware = SessionMiddleware(lambda req: response)

    with pytest.raises(SuspiciousOperation):
        middleware.process_response(request, response)