import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.middleware.security import SecurityMiddleware

def test_security_middleware_init(settings):
    # Set required settings
    settings.SECURE_HSTS_SECONDS = 31536000
    settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    settings.SECURE_HSTS_PRELOAD = True
    settings.SECURE_CONTENT_TYPE_NOSNIFF = True
    settings.SECURE_BROWSER_XSS_FILTER = True
    settings.SECURE_SSL_REDIRECT = True
    settings.SECURE_SSL_HOST = 'example.com'
    settings.SECURE_REDIRECT_EXEMPT = ['test-exempt-url']
    settings.SECURE_REFERRER_POLICY = 'no-referrer'

    middleware = SecurityMiddleware()

    assert middleware.sts_seconds == settings.SECURE_HSTS_SECONDS
    assert middleware.sts_include_subdomains == settings.SECURE_HSTS_INCLUDE_SUBDOMAINS
    assert middleware.sts_preload == settings.SECURE_HSTS_PRELOAD
    assert middleware.content_type_nosniff == settings.SECURE_CONTENT_TYPE_NOSNIFF
    assert middleware.xss_filter == settings.SECURE_BROWSER_XSS_FILTER
    assert middleware.redirect == settings.SECURE_SSL_REDIRECT
    assert middleware.redirect_host == settings.SECURE_SSL_HOST
    assert middleware.redirect_exempt == [re.compile(r) for r in settings.SECURE_REDIRECT_EXEMPT]
    assert middleware.referrer_policy == settings.SECURE_REFERRER_POLICY