import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.middleware.security import SecurityMiddleware

@pytest.mark.parametrize("settings_input, expected_attrs", [
    (
        {
            'SECURE_HSTS_SECONDS': 3600,
            'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
            'SECURE_HSTS_PRELOAD': True,
            'SECURE_CONTENT_TYPE_NOSNIFF': True,
            'SECURE_BROWSER_XSS_FILTER': True,
            'SECURE_SSL_REDIRECT': True,
            'SECURE_SSL_HOST': 'example.com',
            'SECURE_REDIRECT_EXEMPT': [],
            'SECURE_REFERRER_POLICY': 'no-referrer',
        },
        {
            'sts_seconds': 3600,
            'sts_include_subdomains': True,
            'sts_preload': True,
            'content_type_nosniff': True,
            'xss_filter': True,
            'redirect': True,
            'redirect_host': 'example.com',
            'redirect_exempt': [],
            'referrer_policy': 'no-referrer'
        }
    )
])
def test_security_middleware_init(settings_input, expected_attrs):
    for key, value in settings_input.items():
        setattr(settings, key, value)

    middleware = SecurityMiddleware()

    for attr, expected_value in expected_attrs.items():
        assert getattr(middleware, attr) == expected_value