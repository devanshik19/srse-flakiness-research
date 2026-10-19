import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_resolver_match_repr():
    user = User(username='testuser')
    func = 'app_name.view_name'
    args = (1, 'foo')
    kwargs = {'bar': 'baz'}
    url_name = 'test_url'
    app_names = ['app1', 'app2']
    namespaces = ['namespace1', 'namespace2']
    route = '/test/route/'

    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route)

    expected_repr = (
        "ResolverMatch(func=%s, args=%s, kwargs=%s, url_name=%s, app_names=%s, namespaces=%s, route=%s)" % (
            func, args, kwargs, url_name, app_names, namespaces, route
        )
    )

    assert repr(resolver_match) == expected_repr