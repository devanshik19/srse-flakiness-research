import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_getitem():
    # Arrange
    func = lambda x: x
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'test_view'
    app_names = ['app1', 'app2']
    namespaces = ['namespace1']
    route = '/test/'

    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route, [])

    # Act & Assert
    # Testing for index 0 (func)
    assert resolver_match[0] == func
    # Testing for index 1 (args)
    assert resolver_match[1] == args
    # Testing for index 2 (kwargs)
    assert resolver_match[2] == kwargs

    # Testing out-of-bounds index, which should raise an IndexError
    with pytest.raises(IndexError):
        _ = resolver_match[3]