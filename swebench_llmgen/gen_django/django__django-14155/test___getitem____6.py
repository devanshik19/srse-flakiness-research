import pytest
from django.contrib.auth.models import User
from django.urls import ResolverMatch

def test_getitem():
    # Creating a test instance of ResolverMatch with dummy data
    func = lambda: None
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'test-url'
    app_names = ['app1', 'app2']
    namespaces = ['namespace1', 'namespace2']
    route = '/test/path/'
    tried = []

    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route, tried)

    # Testing the __getitem__ method
    assert resolver_match[0] == func  # Testing access to func
    assert resolver_match[1] == args   # Testing access to args
    assert resolver_match[2] == kwargs  # Testing access to kwargs

    # Testing out of range access
    with pytest.raises(IndexError):
        resolver_match[3]