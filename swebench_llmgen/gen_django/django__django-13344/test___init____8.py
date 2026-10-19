import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.middleware.security import SecurityMiddleware

@pytest.mark.parametrize(
    'settings_overrides, expected_sts_seconds',
    [
        ({'SECURE_HSTS_SECONDS': 3600}, 3600),
        ({'SECURE_HSTS_SECONDS': 7200}, 7200),
    ]
)
def test_security_middleware_init(settings_overrides, expected_sts_seconds):
    for key, value in settings_overrides.items():
        setattr(settings, key, value)

    middleware = SecurityMiddleware()
    
    assert middleware.sts_seconds == expected_sts_seconds
    assert middleware.sts_include_subdomains == getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
    assert middleware.sts_preload == getattr(settings, 'SECURE_HSTS_PRELOAD', False)
    assert middleware.content_type_nosniff == getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False)
    assert middleware.xss_filter == getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False)
    assert middleware.redirect == getattr(settings, 'SECURE_SSL_REDIRECT', False)
    assert middleware.redirect_host == getattr(settings, 'SECURE_SSL_HOST', None)
    assert isinstance(middleware.redirect_exempt, list)
    assert isinstance(middleware.redirect_exempt, list)
    assert middleware.referrer_policy == getattr(settings, 'SECURE_REFERRER_POLICY', None)