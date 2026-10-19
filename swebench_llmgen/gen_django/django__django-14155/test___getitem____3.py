import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_resolver_match_getitem():
    # Arrange
    func = lambda x: x  # A simple function for testing
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'test_view'
    app_names = ['app1', 'app2']
    namespaces = ['namespace1', 'namespace2']
    route = '/test/route/'
    tried = []

    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route, tried)

    # Act & Assert
    # Test accessing the function
    assert resolver_match[0] == func
    # Test accessing the args
    assert resolver_match[1] == args
    # Test accessing the kwargs
    assert resolver_match[2] == kwargs

    # Test out of bounds index
    with pytest.raises(IndexError):
        _ = resolver_match[3]
        
    # Test negative indexing for last item
    assert resolver_match[-1] == kwargs