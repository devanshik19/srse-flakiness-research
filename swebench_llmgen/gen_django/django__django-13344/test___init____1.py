import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.middleware.security import SecurityMiddleware

@pytest.fixture
def set_secure_settings():
    settings.SECURE_HSTS_SECONDS = 3600
    settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    settings.SECURE_HSTS_PRELOAD = True
    settings.SECURE_CONTENT_TYPE_NOSNIFF = True
    settings.SECURE_BROWSER_XSS_FILTER = True
    settings.SECURE_SSL_REDIRECT = True
    settings.SECURE_SSL_HOST = 'example.com'
    settings.SECURE_REDIRECT_EXEMPT = []
    settings.SECURE_REFERRER_POLICY = 'same-origin'

def test_security_middleware_init(set_secure_settings):
    middleware = SecurityMiddleware()

    assert middleware.sts_seconds == 3600
    assert middleware.sts_include_subdomains is True
    assert middleware.sts_preload is True
    assert middleware.content_type_nosniff is True
    assert middleware.xss_filter is True
    assert middleware.redirect is True
    assert middleware.redirect_host == 'example.com'
    assert middleware.redirect_exempt == []
    assert middleware.referrer_policy == 'same-origin'