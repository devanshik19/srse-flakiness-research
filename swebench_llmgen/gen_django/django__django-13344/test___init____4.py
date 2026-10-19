import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.middleware.security import SecurityMiddleware

@pytest.fixture
def security_middleware():
    return SecurityMiddleware()

def test_security_middleware_init(security_middleware):
    assert security_middleware.sts_seconds == settings.SECURE_HSTS_SECONDS
    assert security_middleware.sts_include_subdomains == settings.SECURE_HSTS_INCLUDE_SUBDOMAINS
    assert security_middleware.sts_preload == settings.SECURE_HSTS_PRELOAD
    assert security_middleware.content_type_nosniff == settings.SECURE_CONTENT_TYPE_NOSNIFF
    assert security_middleware.xss_filter == settings.SECURE_BROWSER_XSS_FILTER
    assert security_middleware.redirect == settings.SECURE_SSL_REDIRECT
    assert security_middleware.redirect_host == settings.SECURE_SSL_HOST
    assert security_middleware.redirect_exempt == [re.compile(r) for r in settings.SECURE_REDIRECT_EXEMPT]
    assert security_middleware.referrer_policy == settings.SECURE_REFERRER_POLICY
    assert security_middleware.get_response is None