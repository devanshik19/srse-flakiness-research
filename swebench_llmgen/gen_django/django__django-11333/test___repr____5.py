import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_resolver_match_repr():
    func = User
    args = (1,)
    kwargs = {'key': 'value'}
    url_name = 'test_url'
    app_names = ['app1', 'app2']
    namespaces = ['namespace1', 'namespace2']
    route = '/test/'

    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route)

    expected_repr = (
        "ResolverMatch(func=<class 'django.contrib.auth.models.User'>, args=(1,), "
        "kwargs={'key': 'value'}, url_name=test_url, "
        "app_names=['app1', 'app2'], namespaces=['namespace1', 'namespace2'], route=/test/)"
    )

    assert repr(resolver_match) == expected_repr