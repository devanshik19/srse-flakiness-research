import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.middleware.security import SecurityMiddleware

@pytest.fixture
def setup_settings():
    settings.SECURE_HSTS_SECONDS = 3600
    settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    settings.SECURE_HSTS_PRELOAD = True
    settings.SECURE_CONTENT_TYPE_NOSNIFF = True
    settings.SECURE_BROWSER_XSS_FILTER = True
    settings.SECURE_SSL_REDIRECT = True
    settings.SECURE_SSL_HOST = None
    settings.SECURE_REDIRECT_EXEMPT = []
    settings.SECURE_REFERRER_POLICY = 'no-referrer'

def test_security_middleware_init(setup_settings):
    mw = SecurityMiddleware()
    assert mw.sts_seconds == 3600
    assert mw.sts_include_subdomains is True
    assert mw.sts_preload is True
    assert mw.content_type_nosniff is True
    assert mw.xss_filter is True
    assert mw.redirect is True
    assert mw.redirect_host is None
    assert mw.redirect_exempt == []
    assert mw.referrer_policy == 'no-referrer'