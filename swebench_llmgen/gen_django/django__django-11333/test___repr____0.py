import pytest
from django.contrib.auth.models import User
from django.urls import resolve
from django.urls.resolvers import ResolverMatch

def test_resolver_match_repr():
    func = lambda request: None  # Dummy callable
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'test-url'
    app_names = ['app1', 'app2']
    namespaces = ['namespace1', 'namespace2']
    route = '/test-route/'

    match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route)

    expected_repr = (
        "ResolverMatch(func=<function test_resolver_match_repr.<locals>.<lambda> at "
        f"{hex(id(func))}, args=(1, 2, 3), kwargs={{'key': 'value'}}, url_name='test-url', "
        "app_names=['app1', 'app2'], namespaces=['namespace1', 'namespace2'], "
        "route='/test-route/')"
    )

    assert repr(match) == expected_repr