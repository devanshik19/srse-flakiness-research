import pytest
from django.contrib.auth.models import User
from django.urls import ResolverMatch

def test_getitem():
    # Arrange
    func = lambda x: x
    args = (1, 2, 3)
    kwargs = {'key': 'value'}
    url_name = 'test-name'
    app_names = ['test-app']
    namespaces = ['test-namespace']
    route = '/test/url/'
    tried = []

    resolver_match = ResolverMatch(func, args, kwargs, url_name, app_names, namespaces, route, tried)

    # Act
    func_result = resolver_match[0]
    args_result = resolver_match[1]
    kwargs_result = resolver_match[2]

    # Assert
    assert func_result == func
    assert args_result == args
    assert kwargs_result == kwargs

    # Test invalid index access
    with pytest.raises(IndexError):
        resolver_match[3]