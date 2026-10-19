import pytest
from django.contrib.auth.models import User
from django.urls.resolvers import ResolverMatch

def test_getitem():
    # Create a mock function and parameters
    def mock_view(request, *args, **kwargs):
        return "mock response"

    func = mock_view
    args = (1, 2, 3)
    kwargs = {'a': 4, 'b': 5}
    url_name = 'mock_url_name'
    app_names = ['mock_app']
    namespaces = ['mock_namespace']
    route = '/mock/route/'

    # Create an instance of ResolverMatch
    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route, [])

    # Test __getitem__ for func, args, kwargs
    assert resolver_match[0] == func, "Failed to retrieve func"
    assert resolver_match[1] == args, "Failed to retrieve args"
    assert resolver_match[2] == kwargs, "Failed to retrieve kwargs"
    
    # Test index out of range
    with pytest.raises(IndexError):
        _ = resolver_match[3]