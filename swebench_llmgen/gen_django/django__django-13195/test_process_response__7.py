import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.conf import settings

class TestSessionMiddleware:
    def setup_method(self):
        self.middleware = SessionMiddleware(lambda request: HttpResponse())
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.request = HttpRequest()
        self.request.session = self.user.session_set.create(session_key='testkey')

    def test_process_response_no_session(self):
        response = self.middleware.process_response(self.request, HttpResponse())
        assert response.status_code == 200

    def test_process_response_session_empty(self):
        self.request.session.set_decoded({})
        response = self.middleware.process_response(self.request, HttpResponse())
        assert settings.SESSION_COOKIE_NAME not in response.cookies

    def test_process_response_session_modified(self):
        self.request.session.modified = True
        response = self.middleware.process_response(self.request, HttpResponse())
        assert response.cookies[settings.SESSION_COOKIE_NAME].value == self.request.session.session_key

    def test_process_response_session_accessed(self):
        self.request.session.accessed = True
        response = self.middleware.process_response(self.request, HttpResponse())
        assert settings.SESSION_COOKIE_NAME in response.cookies

    def test_process_response_save_on_every_request(self):
        settings.SESSION_SAVE_EVERY_REQUEST = True
        self.request.session.modified = False
        response = self.middleware.process_response(self.request, HttpResponse())
        assert settings.SESSION_COOKIE_NAME in response.cookies

    def test_process_response_session_error(self):
        self.request.session = None  # Simulate absence of session
        response = self.middleware.process_response(self.request, HttpResponse())
        assert response.status_code == 200

    def test_process_response_status_code_not_500(self):
        self.request.session.modified = True
        response = self.middleware.process_response(self.request, HttpResponse(status=200))
        assert response.cookies[settings.SESSION_COOKIE_NAME].value == self.request.session.session_key

    def test_process_response_status_code_500(self):
        self.request.session.modified = True
        response = self.middleware.process_response(self.request, HttpResponse(status=500))
        assert settings.SESSION_COOKIE_NAME not in response.cookies