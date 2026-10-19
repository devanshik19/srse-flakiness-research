import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.middleware.security import SecurityMiddleware

@pytest.mark.parametrize("secure_hsts_seconds, secure_hsts_include_subdomains, secure_hsts_preload, secure_content_type_nosniff, secure_browser_xss_filter, secure_ssl_redirect, secure_ssl_host, secure_redirect_exempt, secure_referrer_policy", [
    (60, True, True, True, True, True, None, [], 'no-referrer'),
    (0, False, False, False, False, False, 'localhost', ['admin'], 'no-referrer-when-downgrade'),
])
def test_security_middleware_init(settings, secure_hsts_seconds, secure_hsts_include_subdomains, secure_hsts_preload, secure_content_type_nosniff, secure_browser_xss_filter, secure_ssl_redirect, secure_ssl_host, secure_redirect_exempt, secure_referrer_policy):
    settings.SECURE_HSTS_SECONDS = secure_hsts_seconds
    settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = secure_hsts_include_subdomains
    settings.SECURE_HSTS_PRELOAD = secure_hsts_preload
    settings.SECURE_CONTENT_TYPE_NOSNIFF = secure_content_type_nosniff
    settings.SECURE_BROWSER_XSS_FILTER = secure_browser_xss_filter
    settings.SECURE_SSL_REDIRECT = secure_ssl_redirect
    settings.SECURE_SSL_HOST = secure_ssl_host
    settings.SECURE_REDIRECT_EXEMPT = secure_redirect_exempt
    settings.SECURE_REFERRER_POLICY = secure_referrer_policy

    middleware = SecurityMiddleware(get_response=None)

    assert middleware.sts_seconds == secure_hsts_seconds
    assert middleware.sts_include_subdomains == secure_hsts_include_subdomains
    assert middleware.sts_preload == secure_hsts_preload
    assert middleware.content_type_nosniff == secure_content_type_nosniff
    assert middleware.xss_filter == secure_browser_xss_filter
    assert middleware.redirect == secure_ssl_redirect
    assert middleware.redirect_host == secure_ssl_host
    assert middleware.redirect_exempt == [re.compile(r) for r in secure_redirect_exempt]
    assert middleware.referrer_policy == secure_referrer_policy