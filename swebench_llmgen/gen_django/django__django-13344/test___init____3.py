import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.middleware.security import SecurityMiddleware

@pytest.mark.parametrize("setting_name, setting_value", [
    ("SECURE_HSTS_SECONDS", 3600),
    ("SECURE_HSTS_INCLUDE_SUBDOMAINS", True),
    ("SECURE_HSTS_PRELOAD", True),
    ("SECURE_CONTENT_TYPE_NOSNIFF", True),
    ("SECURE_BROWSER_XSS_FILTER", True),
    ("SECURE_SSL_REDIRECT", True),
    ("SECURE_SSL_HOST", "example.com"),
    ("SECURE_REDIRECT_EXEMPT", []),
    ("SECURE_REFERRER_POLICY", "same-origin")
])
def test_security_middleware_init(settings, setting_name, setting_value):
    setattr(settings, setting_name, setting_value)

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
    assert middleware.get_response is None