import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
from django.middleware.security import SecurityMiddleware

@pytest.fixture
def custom_settings():
    class Settings:
        SECURE_HSTS_SECONDS = 3600
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True
        SECURE_CONTENT_TYPE_NOSNIFF = True
        SECURE_BROWSER_XSS_FILTER = True
        SECURE_SSL_REDIRECT = True
        SECURE_SSL_HOST = 'www.example.com'
        SECURE_REDIRECT_EXEMPT = ['^/ignore/', '^/test/']
        SECURE_REFERRER_POLICY = 'no-referrer'
    
    return Settings()

def test_security_middleware_init(custom_settings, monkeypatch):
    # Patch settings for the test
    monkeypatch.setattr(settings, 'SECURE_HSTS_SECONDS', custom_settings.SECURE_HSTS_SECONDS)
    monkeypatch.setattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', custom_settings.SECURE_HSTS_INCLUDE_SUBDOMAINS)
    monkeypatch.setattr(settings, 'SECURE_HSTS_PRELOAD', custom_settings.SECURE_HSTS_PRELOAD)
    monkeypatch.setattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', custom_settings.SECURE_CONTENT_TYPE_NOSNIFF)
    monkeypatch.setattr(settings, 'SECURE_BROWSER_XSS_FILTER', custom_settings.SECURE_BROWSER_XSS_FILTER)
    monkeypatch.setattr(settings, 'SECURE_SSL_REDIRECT', custom_settings.SECURE_SSL_REDIRECT)
    monkeypatch.setattr(settings, 'SECURE_SSL_HOST', custom_settings.SECURE_SSL_HOST)
    monkeypatch.setattr(settings, 'SECURE_REDIRECT_EXEMPT', custom_settings.SECURE_REDIRECT_EXEMPT)
    monkeypatch.setattr(settings, 'SECURE_REFERRER_POLICY', custom_settings.SECURE_REFERRER_POLICY)

    # Instantiate the middleware
    middleware = SecurityMiddleware()

    # Assert the values are set correctly
    assert middleware.sts_seconds == custom_settings.SECURE_HSTS_SECONDS
    assert middleware.sts_include_subdomains == custom_settings.SECURE_HSTS_INCLUDE_SUBDOMAINS
    assert middleware.sts_preload == custom_settings.SECURE_HSTS_PRELOAD
    assert middleware.content_type_nosniff == custom_settings.SECURE_CONTENT_TYPE_NOSNIFF
    assert middleware.xss_filter == custom_settings.SECURE_BROWSER_XSS_FILTER
    assert middleware.redirect == custom_settings.SECURE_SSL_REDIRECT
    assert middleware.redirect_host == custom_settings.SECURE_SSL_HOST
    assert len(middleware.redirect_exempt) == len(custom_settings.SECURE_REDIRECT_EXEMPT)
    assert middleware.referrer_policy == custom_settings.SECURE_REFERRER_POLICY